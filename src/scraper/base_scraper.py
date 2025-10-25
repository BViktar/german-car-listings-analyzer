"""
Base scraper class for German car listings.

This module provides a base class for implementing scrapers for different
German automotive marketplaces.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    # Dependencies will be installed via requirements.txt
    pass

from src.config import Config


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for car listing scrapers."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the scraper.
        
        Args:
            base_url: Base URL of the marketplace. If not provided,
                     subclass should set it.
        """
        self.base_url = base_url
        self.session = self._create_session()
        self.config = Config.SCRAPING
    
    def _create_session(self) -> 'requests.Session':
        """
        Create and configure a requests session.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.config['user_agent']
        })
        return session
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        Make a GET request with retry logic.
        
        Args:
            url: URL to request
            params: Optional query parameters
        
        Returns:
            Response text if successful, None otherwise
        """
        for attempt in range(self.config['retry_attempts']):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.config['timeout']
                )
                response.raise_for_status()
                
                # Delay between requests to be respectful
                time.sleep(self.config['delay_between_requests'])
                
                return response.text
                
            except Exception as e:
                logger.warning(
                    f"Request attempt {attempt + 1} failed for {url}: {str(e)}"
                )
                if attempt < self.config['retry_attempts'] - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed for {url}")
                    return None
    
    def _parse_html(self, html: str) -> Optional['BeautifulSoup']:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html: HTML content to parse
        
        Returns:
            BeautifulSoup object or None if parsing fails
        """
        try:
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            logger.error(f"Failed to parse HTML: {str(e)}")
            return None
    
    @abstractmethod
    def scrape_listings(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape car listings based on search parameters.
        
        This method must be implemented by subclasses for specific marketplaces.
        
        Args:
            search_params: Dictionary of search parameters (make, model, year, etc.)
        
        Returns:
            List of listing dictionaries
        """
        pass
    
    @abstractmethod
    def parse_listing_page(self, soup: 'BeautifulSoup') -> List[Dict[str, Any]]:
        """
        Parse a listings page and extract listing data.
        
        This method must be implemented by subclasses for specific marketplaces.
        
        Args:
            soup: BeautifulSoup object of the page
        
        Returns:
            List of listing dictionaries
        """
        pass
    
    def get_listing_details(self, listing_url: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific listing.
        
        Args:
            listing_url: URL of the listing
        
        Returns:
            Dictionary with detailed listing information or None
        """
        html = self._make_request(listing_url)
        if not html:
            return None
        
        soup = self._parse_html(html)
        if not soup:
            return None
        
        return self.parse_listing_details(soup)
    
    @abstractmethod
    def parse_listing_details(self, soup: 'BeautifulSoup') -> Dict[str, Any]:
        """
        Parse detailed information from a listing page.
        
        This method must be implemented by subclasses for specific marketplaces.
        
        Args:
            soup: BeautifulSoup object of the listing page
        
        Returns:
            Dictionary with detailed listing information
        """
        pass
