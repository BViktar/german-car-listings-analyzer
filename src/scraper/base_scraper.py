"""Base scraper class with common functionality."""

import logging
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src.config import SCRAPING_CONFIG, EXTRACTION_FIELDS
from src.utils.browser import BrowserManager, random_delay

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for car listing scrapers.
    
    Provides common functionality for scraping car listings including
    rate limiting, error handling, and retry logic.
    """
    
    def __init__(self, browser_manager: Optional[BrowserManager] = None):
        """
        Initialize the base scraper.
        
        Args:
            browser_manager: BrowserManager instance (creates new if None)
        """
        self.browser_manager = browser_manager or BrowserManager(
            headless=SCRAPING_CONFIG["headless"],
            browser_type=SCRAPING_CONFIG["browser_type"]
        )
        self.own_browser = browser_manager is None
        self.max_retries = SCRAPING_CONFIG["max_retries"]
        self.retry_delay = SCRAPING_CONFIG["retry_delay"]
        self.results: List[Dict[str, Any]] = []
    
    @abstractmethod
    def get_site_name(self) -> str:
        """
        Get the name of the website being scraped.
        
        Returns:
            Site name
        """
        pass
    
    @abstractmethod
    def build_search_url(self, **kwargs) -> str:
        """
        Build the search URL with given parameters.
        
        Args:
            **kwargs: Search parameters
            
        Returns:
            Complete search URL
        """
        pass
    
    @abstractmethod
    def extract_listing_data(self, page: Page, listing_element: Any) -> Dict[str, Any]:
        """
        Extract data from a single listing element.
        
        Args:
            page: Playwright page object
            listing_element: Listing element to extract data from
            
        Returns:
            Dictionary containing extracted listing data
        """
        pass
    
    @abstractmethod
    def get_listing_elements(self, page: Page) -> List[Any]:
        """
        Get all listing elements from the current page.
        
        Args:
            page: Playwright page object
            
        Returns:
            List of listing elements
        """
        pass
    
    @abstractmethod
    def has_next_page(self, page: Page) -> bool:
        """
        Check if there is a next page of results.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if next page exists, False otherwise
        """
        pass
    
    @abstractmethod
    def go_to_next_page(self, page: Page) -> bool:
        """
        Navigate to the next page of results.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if navigation successful, False otherwise
        """
        pass
    
    def scrape(
        self,
        search_params: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Main scraping method.
        
        Args:
            search_params: Search parameters for building URL
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of scraped listings
        """
        search_params = search_params or {}
        max_pages = max_pages or SCRAPING_CONFIG["max_pages"]
        
        logger.info(f"Starting scrape on {self.get_site_name()}")
        logger.info(f"Search parameters: {search_params}")
        logger.info(f"Max pages: {max_pages}")
        
        self.results = []
        
        try:
            if self.own_browser:
                self.browser_manager.start()
            
            with self.browser_manager.get_page() as page:
                # Build and navigate to search URL
                search_url = self.build_search_url(**search_params)
                logger.info(f"Navigating to: {search_url}")
                
                self._navigate_with_retry(page, search_url)
                
                # Scrape pages
                page_count = 0
                while page_count < max_pages:
                    page_count += 1
                    logger.info(f"Scraping page {page_count}/{max_pages}")
                    
                    # Extract listings from current page
                    listings_on_page = self._scrape_page(page)
                    logger.info(f"Extracted {listings_on_page} listings from page {page_count}")
                    
                    # Check for next page
                    if page_count < max_pages and self.has_next_page(page):
                        random_delay()
                        if not self.go_to_next_page(page):
                            logger.warning("Failed to navigate to next page, stopping")
                            break
                    else:
                        logger.info("No more pages available")
                        break
                
                logger.info(f"Scraping completed. Total listings: {len(self.results)}")
                
        except Exception as e:
            logger.error(f"Error during scraping: {e}", exc_info=True)
            raise
        finally:
            if self.own_browser:
                self.browser_manager.stop()
        
        return self.results
    
    def _scrape_page(self, page: Page) -> int:
        """
        Scrape all listings from the current page.
        
        Args:
            page: Playwright page object
            
        Returns:
            Number of listings extracted
        """
        count = 0
        
        try:
            # Wait for listings to load
            time.sleep(2)  # Give page time to fully render
            
            # Get all listing elements
            listing_elements = self.get_listing_elements(page)
            logger.debug(f"Found {len(listing_elements)} listing elements")
            
            # Extract data from each listing
            for element in listing_elements:
                try:
                    listing_data = self.extract_listing_data(page, element)
                    if listing_data:
                        self.results.append(listing_data)
                        count += 1
                except Exception as e:
                    logger.warning(f"Failed to extract listing data: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping page: {e}")
        
        return count
    
    def _navigate_with_retry(self, page: Page, url: str) -> None:
        """
        Navigate to URL with retry logic.
        
        Args:
            page: Playwright page object
            url: URL to navigate to
            
        Raises:
            Exception: If all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                page.goto(url, wait_until="domcontentloaded")
                logger.debug(f"Successfully navigated to {url}")
                return
            except PlaywrightTimeoutError as e:
                logger.warning(f"Navigation timeout (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
            except Exception as e:
                logger.error(f"Navigation error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
    
    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get the scraped results.
        
        Returns:
            List of scraped listings
        """
        return self.results
    
    def clear_results(self) -> None:
        """Clear the scraped results."""
        self.results = []
