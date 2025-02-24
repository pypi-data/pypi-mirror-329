import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Route, Request
from fake_useragent import UserAgent
from .models import ScrapeConfig
from .exceptions import ScraperException
from .utils import ContentCleaner
from typing import Dict, Any, Optional
from .config import Config
import logging
from urllib.parse import urlparse
from .extractor import LLMExtractor

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.user_agent = UserAgent().random

    async def initialize(self, config):
        """Initialize the browser and context with robust settings"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=config.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-gpu',
                    '--disable-http2'
                ]
            )

            self.context = await self.browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1920, "height": 1080},
                ignore_https_errors=True,
                java_script_enabled=True,
                bypass_csp=True,
                extra_http_headers=Config.DEFAULT_HEADERS
            )
        except Exception as e:
            raise ScraperException(f"Failed to initialize scraper: {str(e)}")

    async def setup_page_blocking(self, page: Page, config: ScrapeConfig):
        """Setup page-level request blocking"""
        if config.media and config.media.block_loading:
            await page.route(
                "**/*.{png,jpg,jpeg,gif,svg,mp3,mp4,avi,flac,ogg,wav,webm,webp}",
                lambda route: route.abort()
            )

        if config.block_ads:
            async def handle_route(route: Route, request: Request):
                url = urlparse(request.url)
                if any(domain in url.hostname for domain in Config.AD_SERVING_DOMAINS):
                    logger.info(f"Blocked ad domain: {url.hostname}")
                    await route.abort()
                else:
                    await route.continue_()

            await page.route("**/*", handle_route)

    async def scrape(self, config: ScrapeConfig) -> Dict[str, Any]:
        """Main scraping method with comprehensive error handling and cleaning"""
        if not self.context:
            await self.initialize(config)

        page = await self.context.new_page()
        await self.setup_page_blocking(page, config)

        if config.custom_headers:
            await page.set_extra_http_headers(config.custom_headers)

        try:
            logger.info(f'Starting page load for URL: {config.url}')
            response = await page.goto(
                config.url,
                wait_until='domcontentloaded',
                timeout=config.timeout or 30000
            )
            status_code = response.status if response else 0

            if config.wait_after_load:
                await page.wait_for_timeout(config.wait_after_load)

            if config.check_selector:
                await page.wait_for_selector(
                    config.check_selector,
                    timeout=config.timeout
                )

            raw_content = await page.content()
            cleaner = ContentCleaner(raw_content, config.url)
            content = cleaner.clean(config)
            # print("content: ", content
            #       )
            result = {
                'content': content,
                'status_code': status_code
            }
            # print(result)

            if config.extract:
                extractor = LLMExtractor()
                extracted_data = await extractor.extract(content, config.extract)
                result['extracted_data'] = extracted_data

            return result

        except Exception as e:
            logger.error(f'Scraping failed: {str(e)}')
            raise ScraperException(f"Scraping failed: {str(e)}", status_code)
        finally:
            await page.close()

    async def cleanup(self):
        """Cleanup browser resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()