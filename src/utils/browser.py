"""Browser session management utilities."""

import logging
import random
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from fake_useragent import UserAgent

from src.config import SCRAPING_CONFIG, USE_PROXY, PROXY_URL

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Manages browser sessions with anti-bot measures.
    
    Handles browser initialization, user agent rotation, proxy configuration,
    and provides context managers for safe browser usage.
    """
    
    def __init__(
        self,
        headless: bool = True,
        browser_type: str = "chromium",
        use_proxy: bool = False,
        proxy_url: Optional[str] = None,
    ):
        """
        Initialize the BrowserManager.
        
        Args:
            headless: Whether to run browser in headless mode
            browser_type: Type of browser ('chromium', 'firefox', 'webkit')
            use_proxy: Whether to use a proxy
            proxy_url: Proxy URL if use_proxy is True
        """
        self.headless = headless
        self.browser_type = browser_type
        self.use_proxy = use_proxy or USE_PROXY
        self.proxy_url = proxy_url or PROXY_URL
        self.user_agent_rotator = UserAgent()
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    def get_random_user_agent(self) -> str:
        """
        Get a random user agent string.
        
        Returns:
            Random user agent string
        """
        return self.user_agent_rotator.random
    
    def start(self) -> None:
        """Start the browser session."""
        try:
            logger.info(f"Starting {self.browser_type} browser (headless={self.headless})")
            self.playwright = sync_playwright().start()
            
            # Select browser type
            if self.browser_type == "firefox":
                browser_launcher = self.playwright.firefox
            elif self.browser_type == "webkit":
                browser_launcher = self.playwright.webkit
            else:
                browser_launcher = self.playwright.chromium
            
            # Configure launch options
            launch_options: Dict[str, Any] = {
                "headless": self.headless,
            }
            
            # Add proxy if configured
            if self.use_proxy and self.proxy_url:
                logger.info(f"Using proxy: {self.proxy_url}")
                launch_options["proxy"] = {"server": self.proxy_url}
            
            # Launch browser
            self.browser = browser_launcher.launch(**launch_options)
            
            # Create context with random user agent
            context_options: Dict[str, Any] = {
                "user_agent": self.get_random_user_agent(),
                "viewport": {"width": 1920, "height": 1080},
            }
            
            self.context = self.browser.new_context(**context_options)
            
            # Add anti-detection measures
            self._apply_stealth_mode()
            
            logger.info("Browser started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    def _apply_stealth_mode(self) -> None:
        """Apply stealth measures to avoid detection."""
        if self.context:
            # Add init script to mask automation
            self.context.add_init_script("""
                // Overwrite the navigator.webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });
                
                // Mock languages and plugins
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'de-DE', 'de'],
                });
                
                // Mock permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
                );
            """)
    
    def new_page(self) -> Page:
        """
        Create a new page in the browser context.
        
        Returns:
            New page instance
            
        Raises:
            RuntimeError: If browser is not started
        """
        if not self.context:
            raise RuntimeError("Browser not started. Call start() first.")
        
        page = self.context.new_page()
        
        # Set default timeout
        page.set_default_timeout(
            SCRAPING_CONFIG["page_load_timeout"] * 1000
        )
        
        return page
    
    def stop(self) -> None:
        """Stop the browser session and cleanup resources."""
        try:
            if self.context:
                self.context.close()
                logger.debug("Browser context closed")
            
            if self.browser:
                self.browser.close()
                logger.debug("Browser closed")
            
            if self.playwright:
                self.playwright.stop()
                logger.debug("Playwright stopped")
            
            logger.info("Browser session stopped")
            
        except Exception as e:
            logger.error(f"Error stopping browser: {e}")
    
    @contextmanager
    def get_page(self):
        """
        Context manager for safe page usage.
        
        Yields:
            Page instance
            
        Example:
            with browser_manager.get_page() as page:
                page.goto("https://example.com")
        """
        page = None
        try:
            page = self.new_page()
            yield page
        finally:
            if page:
                page.close()
    
    def __enter__(self):
        """Support using BrowserManager as a context manager."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting context manager."""
        self.stop()


def random_delay(min_seconds: Optional[float] = None, max_seconds: Optional[float] = None) -> None:
    """
    Introduce a random delay to mimic human behavior.
    
    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    """
    min_delay = min_seconds or SCRAPING_CONFIG["request_delay_min"]
    max_delay = max_seconds or SCRAPING_CONFIG["request_delay_max"]
    
    delay = random.uniform(min_delay, max_delay)
    logger.debug(f"Waiting for {delay:.2f} seconds")
    time.sleep(delay)
