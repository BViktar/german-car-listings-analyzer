"""Base scraper abstract class for car listing scrapers."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper(ABC):
    """Abstract base class for car listing scrapers."""
    
    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize the base scraper.
        
        Args:
            rate_limit: Minimum time in seconds between requests (default: 1.0)
        """
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.logger = logging.getLogger(__name__)
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy and headers.
        
        Returns:
            Configured requests Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set user agent and headers to avoid blocking
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        return session
        
    def _make_request(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make an HTTP request with rate limiting and error handling.
        
        Args:
            url: URL to request
            params: Optional query parameters
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If request fails after retries
        """
        # Enforce rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit:
            sleep_time = self.rate_limit - time_since_last_request
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        try:
            self.logger.info(f"Making request to: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
            
    @abstractmethod
    def search_broken_motors(self) -> List[Dict]:
        """
        Search for cars with broken motors.
        
        Returns:
            List of car listings with broken motors
        """
        pass
        
    @abstractmethod
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """
        Search for functional cars above minimum price.
        
        Args:
            min_price: Minimum price threshold
            
        Returns:
            List of functional car listings
        """
        pass
