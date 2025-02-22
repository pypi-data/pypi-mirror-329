from __future__ import annotations

import logging
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Generic

from pydantic import ValidationError
from typing_extensions import NotRequired, TypedDict, TypeVar
from yarl import URL

from crawlee import EnqueueStrategy, RequestTransformAction
from crawlee._request import Request, RequestOptions
from crawlee._utils.blocked import RETRY_CSS_SELECTORS
from crawlee._utils.docs import docs_group
from crawlee._utils.urls import convert_to_absolute_url, is_url_absolute
from crawlee.browsers import BrowserPool
from crawlee.crawlers._basic import BasicCrawler, BasicCrawlerOptions, ContextPipeline
from crawlee.errors import SessionError
from crawlee.statistics import StatisticsState

from ._playwright_crawling_context import PlaywrightCrawlingContext
from ._playwright_pre_nav_crawling_context import PlaywrightPreNavCrawlingContext
from ._utils import block_requests, infinite_scroll

TCrawlingContext = TypeVar('TCrawlingContext', bound=PlaywrightCrawlingContext)
TStatisticsState = TypeVar('TStatisticsState', bound=StatisticsState, default=StatisticsState)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Mapping

    from playwright.async_api import Page
    from typing_extensions import Unpack

    from crawlee._types import BasicCrawlingContext, EnqueueLinksKwargs
    from crawlee.browsers._types import BrowserType
    from crawlee.fingerprint_suite import FingerprintGenerator


@docs_group('Classes')
class PlaywrightCrawler(BasicCrawler[PlaywrightCrawlingContext, StatisticsState]):
    """A web crawler that leverages the `Playwright` browser automation library.

    The `PlaywrightCrawler` builds on top of the `BasicCrawler`, which means it inherits all of its features.
    On top of that it provides a high level web crawling interface on top of the `Playwright` library. To be more
    specific, it uses the Crawlee's `BrowserPool` to manage the Playwright's browser instances and the pages they
    open. You can create your own `BrowserPool` instance and pass it to the `PlaywrightCrawler` constructor, or let
    the crawler create a new instance with the default settings.

    This crawler is ideal for crawling websites that require JavaScript execution, as it uses real browsers
    to download web pages and extract data. For websites that do not require JavaScript, consider using one of the
    HTTP client-based crawlers, such as the `HttpCrawler`, `ParselCrawler`, or `BeautifulSoupCrawler`. They use
    raw HTTP requests, which means they are much faster.

    ### Usage

    ```python
    from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

    crawler = PlaywrightCrawler()

    # Define the default request handler, which will be called for every request.
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')

        # Extract data from the page.
        data = {
            'url': context.request.url,
            'title': await context.page.title(),
            'response': (await context.response.text())[:100],
        }

        # Push the extracted data to the default dataset.
        await context.push_data(data)

    await crawler.run(['https://crawlee.dev/'])
    ```
    """

    def __init__(
        self,
        *,
        browser_pool: BrowserPool | None = None,
        browser_type: BrowserType | None = None,
        browser_launch_options: Mapping[str, Any] | None = None,
        browser_new_context_options: Mapping[str, Any] | None = None,
        fingerprint_generator: FingerprintGenerator | None = None,
        headless: bool | None = None,
        use_incognito_pages: bool | None = None,
        **kwargs: Unpack[BasicCrawlerOptions[PlaywrightCrawlingContext, StatisticsState]],
    ) -> None:
        """A default constructor.

        Args:
            browser_pool: A `BrowserPool` instance to be used for launching the browsers and getting pages.
            browser_type: The type of browser to launch ('chromium', 'firefox', or 'webkit').
                This option should not be used if `browser_pool` is provided.
            browser_launch_options: Keyword arguments to pass to the browser launch method. These options are provided
                directly to Playwright's `browser_type.launch` method. For more details, refer to the
                [Playwright documentation](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch).
                This option should not be used if `browser_pool` is provided.
            browser_new_context_options: Keyword arguments to pass to the browser new context method. These options
                are provided directly to Playwright's `browser.new_context` method. For more details, refer to the
                [Playwright documentation](https://playwright.dev/python/docs/api/class-browser#browser-new-context).
                This option should not be used if `browser_pool` is provided.
            fingerprint_generator: An optional instance of implementation of `FingerprintGenerator` that is used
                to generate browser fingerprints together with consistent headers.
            headless: Whether to run the browser in headless mode.
                This option should not be used if `browser_pool` is provided.
            use_incognito_pages: By default pages share the same browser context. If set to True each page uses its
                own context that is destroyed once the page is closed or crashes.
                This option should not be used if `browser_pool` is provided.
            kwargs: Additional keyword arguments to pass to the underlying `BasicCrawler`.
        """
        if browser_pool:
            # Raise an exception if browser_pool is provided together with other browser-related arguments.
            if any(
                param is not None
                for param in (
                    use_incognito_pages,
                    headless,
                    browser_type,
                    browser_launch_options,
                    browser_new_context_options,
                    fingerprint_generator,
                )
            ):
                raise ValueError(
                    'You cannot provide `headless`, `browser_type`, `browser_launch_options`, '
                    '`browser_new_context_options`, `use_incognito_pages`  or `fingerprint_generator` arguments when '
                    '`browser_pool` is provided.'
                )

        # If browser_pool is not provided, create a new instance of BrowserPool with specified arguments.
        else:
            browser_pool = BrowserPool.with_default_plugin(
                headless=headless,
                browser_type=browser_type,
                browser_launch_options=browser_launch_options,
                browser_new_context_options=browser_new_context_options,
                use_incognito_pages=use_incognito_pages,
                fingerprint_generator=fingerprint_generator,
            )

        self._browser_pool = browser_pool

        # Compose the context pipeline with the Playwright-specific context enhancer.
        kwargs['_context_pipeline'] = (
            ContextPipeline().compose(self._open_page).compose(self._navigate).compose(self._handle_blocked_request)
        )
        kwargs['_additional_context_managers'] = [self._browser_pool]
        kwargs.setdefault('_logger', logging.getLogger(__name__))
        self._pre_navigation_hooks: list[Callable[[PlaywrightPreNavCrawlingContext], Awaitable[None]]] = []

        super().__init__(**kwargs)

    async def _open_page(
        self,
        context: BasicCrawlingContext,
    ) -> AsyncGenerator[PlaywrightPreNavCrawlingContext, None]:
        if self._browser_pool is None:
            raise ValueError('Browser pool is not initialized.')

        # Create a new browser page
        crawlee_page = await self._browser_pool.new_page(proxy_info=context.proxy_info)

        pre_navigation_context = PlaywrightPreNavCrawlingContext(
            request=context.request,
            session=context.session,
            add_requests=context.add_requests,
            send_request=context.send_request,
            push_data=context.push_data,
            use_state=context.use_state,
            proxy_info=context.proxy_info,
            get_key_value_store=context.get_key_value_store,
            log=context.log,
            page=crawlee_page.page,
            block_requests=partial(block_requests, page=crawlee_page.page),
        )

        for hook in self._pre_navigation_hooks:
            await hook(pre_navigation_context)

        yield pre_navigation_context

    async def _navigate(
        self,
        context: PlaywrightPreNavCrawlingContext,
    ) -> AsyncGenerator[PlaywrightCrawlingContext, None]:
        """Executes an HTTP request utilizing the `BrowserPool` and the `Playwright` library.

        Args:
            context: The basic crawling context to be enhanced.

        Raises:
            ValueError: If the browser pool is not initialized.
            SessionError: If the URL cannot be loaded by the browser.

        Yields:
            The enhanced crawling context with the Playwright-specific features (page, response, enqueue_links,
                infinite_scroll and block_requests).
        """
        async with context.page:
            if context.session:
                await self._set_cookies(context.page, context.request.url, context.session.cookies)

            if context.request.headers:
                await context.page.set_extra_http_headers(context.request.headers.model_dump())
            # Navigate to the URL and get response.
            response = await context.page.goto(context.request.url)

            if response is None:
                raise SessionError(f'Failed to load the URL: {context.request.url}')

            # Set the loaded URL to the actual URL after redirection.
            context.request.loaded_url = context.page.url

            if context.session:
                cookies = await self._get_cookies(context.page)
                context.session.cookies.update(cookies)

            async def enqueue_links(
                *,
                selector: str = 'a',
                label: str | None = None,
                user_data: dict | None = None,
                transform_request_function: Callable[[RequestOptions], RequestOptions | RequestTransformAction]
                | None = None,
                **kwargs: Unpack[EnqueueLinksKwargs],
            ) -> None:
                """The `PlaywrightCrawler` implementation of the `EnqueueLinksFunction` function."""
                kwargs.setdefault('strategy', EnqueueStrategy.SAME_HOSTNAME)

                requests = list[Request]()
                base_user_data = user_data or {}

                elements = await context.page.query_selector_all(selector)

                for element in elements:
                    url = await element.get_attribute('href')

                    if url:
                        url = url.strip()

                        if not is_url_absolute(url):
                            base_url = context.request.loaded_url or context.request.url
                            url = convert_to_absolute_url(base_url, url)

                        request_option = RequestOptions({'url': url, 'user_data': {**base_user_data}, 'label': label})

                        if transform_request_function:
                            transform_request_option = transform_request_function(request_option)
                            if transform_request_option == 'skip':
                                continue
                            if transform_request_option != 'unchanged':
                                request_option = transform_request_option

                        try:
                            request = Request.from_url(**request_option)
                        except ValidationError as exc:
                            context.log.debug(
                                f'Skipping URL "{url}" due to invalid format: {exc}. '
                                'This may be caused by a malformed URL or unsupported URL scheme. '
                                'Please ensure the URL is correct and retry.'
                            )
                            continue

                        requests.append(request)

                await context.add_requests(requests, **kwargs)

            yield PlaywrightCrawlingContext(
                request=context.request,
                session=context.session,
                add_requests=context.add_requests,
                send_request=context.send_request,
                push_data=context.push_data,
                use_state=context.use_state,
                proxy_info=context.proxy_info,
                get_key_value_store=context.get_key_value_store,
                log=context.log,
                page=context.page,
                infinite_scroll=lambda: infinite_scroll(context.page),
                response=response,
                enqueue_links=enqueue_links,
                block_requests=partial(block_requests, page=context.page),
            )

    async def _handle_blocked_request(
        self,
        context: PlaywrightCrawlingContext,
    ) -> AsyncGenerator[PlaywrightCrawlingContext, None]:
        """Try to detect if the request is blocked based on the HTTP status code or the response content.

        Args:
            context: The current crawling context.

        Raises:
            SessionError: If the request is considered blocked.

        Yields:
            The original crawling context if no errors are detected.
        """
        if self._retry_on_blocked:
            status_code = context.response.status

            # Check if the session is blocked based on the HTTP status code.
            if self._is_session_blocked_status_code(context.session, status_code):
                raise SessionError(f'Assuming the session is blocked based on HTTP status code {status_code}')

            matched_selectors = [
                selector for selector in RETRY_CSS_SELECTORS if (await context.page.query_selector(selector))
            ]

            # Check if the session is blocked based on the response content
            if matched_selectors:
                raise SessionError(
                    'Assuming the session is blocked - '
                    f"HTTP response matched the following selectors: {'; '.join(matched_selectors)}"
                )

        yield context

    def pre_navigation_hook(self, hook: Callable[[PlaywrightPreNavCrawlingContext], Awaitable[None]]) -> None:
        """Register a hook to be called before each navigation.

        Args:
            hook: A coroutine function to be called before each navigation.
        """
        self._pre_navigation_hooks.append(hook)

    async def _get_cookies(self, page: Page) -> dict[str, str]:
        """Get the cookies from the page."""
        cookies = await page.context.cookies()
        return {cookie['name']: cookie['value'] for cookie in cookies if cookie.get('name') and cookie.get('value')}

    async def _set_cookies(self, page: Page, url: str, cookies: dict[str, str]) -> None:
        """Set the cookies to the page."""
        parsed_url = URL(url)
        await page.context.add_cookies(
            [{'name': name, 'value': value, 'domain': parsed_url.host, 'path': '/'} for name, value in cookies.items()]
        )


class _PlaywrightCrawlerAdditionalOptions(TypedDict):
    """Additional arguments for the `PlaywrightCrawler` constructor.

    It is intended for typing forwarded `__init__` arguments in the subclasses.
    All arguments are `BasicCrawlerOptions` + `_PlaywrightCrawlerAdditionalOptions`
    """

    browser_pool: NotRequired[BrowserPool]
    """A `BrowserPool` instance to be used for launching the browsers and getting pages."""

    browser_type: NotRequired[BrowserType]
    """The type of browser to launch ('chromium', 'firefox', or 'webkit').
    This option should not be used if `browser_pool` is provided."""

    browser_launch_options: NotRequired[Mapping[str, Any]]
    """Keyword arguments to pass to the browser launch method. These options are provided
    directly to Playwright's `browser_type.launch` method. For more details, refer to the Playwright
    documentation: https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch.
    This option should not be used if `browser_pool` is provided."""

    browser_new_context_options: NotRequired[Mapping[str, Any]]
    """Keyword arguments to pass to the browser new context method. These options are provided directly to Playwright's
    `browser.new_context` method. For more details, refer to the Playwright documentation:
    https://playwright.dev/python/docs/api/class-browser#browser-new-context. This option should not be used if
    `browser_pool` is provided."""

    headless: NotRequired[bool]
    """Whether to run the browser in headless mode. This option should not be used if `browser_pool` is provided."""


@docs_group('Data structures')
class PlaywrightCrawlerOptions(
    Generic[TCrawlingContext, TStatisticsState],
    _PlaywrightCrawlerAdditionalOptions,
    BasicCrawlerOptions[TCrawlingContext, StatisticsState],
):
    """Arguments for the `AbstractHttpCrawler` constructor.

    It is intended for typing forwarded `__init__` arguments in the subclasses.
    """
