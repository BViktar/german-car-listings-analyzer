"""Base scraper class for car listing websites."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging
import random
import time


class BaseScraper(ABC):
    """Base class for implementing car listing scrapers."""
    
    def __init__(self):
        """Initialize the base scraper with logging and user agents."""
        self.logger = logging.getLogger(__name__)
        self.session = None
        self.user_agents = self._load_user_agents()
        self.logger.info(f"Initialized {self.__class__.__name__}")
        
    @abstractmethod
    def search_broken_motors(self) -> List[Dict]:
        """Search for cars with broken motors.
        
        Returns:
            List[Dict]: List of car listings with broken motors.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass
        
    @abstractmethod
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """Search for functional cars above minimum price.
        
        Args:
            min_price: Minimum price threshold for functional cars (default: 10000).
            
        Returns:
            List[Dict]: List of functional car listings.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass
        
    def _load_user_agents(self) -> List[str]:
        """Load list of user agents for rotation.
        
        Returns:
            List[str]: List of user agent strings for HTTP requests.
        """
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        ]
        self.logger.debug(f"Loaded {len(user_agents)} user agents")
        return user_agents
        
    def _implement_delay(self):
        """Implement random delay between requests to avoid rate limiting.
        
        Uses a random delay between 1 and 3 seconds to mimic human behavior
        and prevent being blocked by the target website.
        """
        delay = random.uniform(1.0, 3.0)
        self.logger.debug(f"Waiting {delay:.2f} seconds before next request")
        time.sleep(delay)
        
    def _get_random_user_agent(self) -> str:
        """Get a random user agent from the loaded list.
        
        Returns:
            str: A randomly selected user agent string.
        """
        return random.choice(self.user_agents)
        
    def _handle_request_error(self, error: Exception, url: str) -> None:
        """Handle and log request errors.
        
        Args:
            error: The exception that occurred.
            url: The URL that caused the error.
        """
        self.logger.error(f"Error accessing {url}: {str(error)}")
        self.logger.debug(f"Error details: {type(error).__name__}", exc_info=True)
