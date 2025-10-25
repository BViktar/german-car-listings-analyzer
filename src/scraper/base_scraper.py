"""Base scraper abstract class for car listing scrapers."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests
import time
import logging


class BaseScraper(ABC):
    """Abstract base class for car listing scrapers."""
    
    def __init__(self):
        """Initialize the base scraper with common settings."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.logger = logging.getLogger(__name__)
        self.request_delay = 2  # Default delay between requests in seconds
        self.last_request_time = 0
        
    def _make_request(self, url: str, params: Optional[Dict] = None, 
                     headers: Optional[Dict] = None) -> requests.Response:
        """
        Make an HTTP request with rate limiting and error handling.
        
        Args:
            url: The URL to request
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If the request fails
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_delay:
            sleep_time = self.request_delay - time_since_last_request
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        # Merge custom headers with session headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        try:
            self.logger.info(f"Making request to {url}")
            response = self.session.get(url, params=params, headers=request_headers, timeout=30)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout for URL: {url}")
            raise
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for URL: {url}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for URL: {url}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error for URL: {url}: {str(e)}")
            raise
    
    @abstractmethod
    def search_broken_motors(self) -> List[Dict]:
        """Search for cars with broken motors."""
        pass
    
    @abstractmethod
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """Search for functional cars above minimum price."""
        pass
