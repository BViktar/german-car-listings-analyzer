"""AutoScout24.de scraper implementation."""

import logging
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlencode
from playwright.sync_api import Page

from src.scraper.base_scraper import BaseScraper
from src.config import AUTOSCOUT24_SEARCH_URL

logger = logging.getLogger(__name__)


class AutoScout24Scraper(BaseScraper):
    """
    Scraper for AutoScout24.de car listings.
    
    Implements site-specific parsing and data extraction logic for AutoScout24.
    """
    
    def get_site_name(self) -> str:
        """Get the name of the website being scraped."""
        return "AutoScout24.de"
    
    def build_search_url(self, **kwargs) -> str:
        """
        Build the search URL for AutoScout24.
        
        Args:
            **kwargs: Search parameters
                - make: Car manufacturer
                - model: Car model
                - year_min: Minimum year
                - year_max: Maximum year
                - mileage_max: Maximum mileage
                - damaged: Whether to search for damaged cars
                
        Returns:
            Complete search URL
        """
        params = {}
        
        # Add make and model
        if kwargs.get('make'):
            params['mmvmk0'] = kwargs['make']
        if kwargs.get('model'):
            params['mmvmd0'] = kwargs['model']
        
        # Add year range
        if kwargs.get('year_min'):
            params['fregfrom'] = kwargs['year_min']
        if kwargs.get('year_max'):
            params['fregto'] = kwargs['year_max']
        
        # Add mileage
        if kwargs.get('mileage_max'):
            params['kmto'] = kwargs['mileage_max']
        
        # Add damaged filter
        if kwargs.get('damaged', False):
            params['damaged'] = '1'
        
        # Add default sorting
        params['sort'] = 'age'
        params['desc'] = '1'
        
        query_string = urlencode(params) if params else ''
        url = f"{AUTOSCOUT24_SEARCH_URL}?{query_string}" if query_string else AUTOSCOUT24_SEARCH_URL
        
        return url
    
    def get_listing_elements(self, page: Page) -> List[Any]:
        """
        Get all listing elements from the current page.
        
        Args:
            page: Playwright page object
            
        Returns:
            List of listing elements
        """
        try:
            # Wait for listings to appear
            page.wait_for_selector('article[data-item-name="listing-summary-vehicle"]', 
                                  timeout=10000, state='visible')
            
            # Get all listing articles
            elements = page.query_selector_all('article[data-item-name="listing-summary-vehicle"]')
            return elements
        except Exception as e:
            logger.warning(f"Could not find listing elements: {e}")
            return []
    
    def extract_listing_data(self, page: Page, listing_element: Any) -> Dict[str, Any]:
        """
        Extract data from a single AutoScout24 listing element.
        
        Args:
            page: Playwright page object
            listing_element: Listing element to extract data from
            
        Returns:
            Dictionary containing extracted listing data
        """
        data: Dict[str, Any] = {}
        
        try:
            # Extract title
            title_elem = listing_element.query_selector('h2')
            data['title'] = title_elem.inner_text().strip() if title_elem else None
            
            # Extract price
            price_elem = listing_element.query_selector('[data-testid="price-details"]')
            if price_elem:
                price_text = price_elem.inner_text().strip()
                data['price'] = self._parse_price(price_text)
            else:
                data['price'] = None
            
            # Extract URL
            link_elem = listing_element.query_selector('a[href*="/details/"]')
            data['url'] = link_elem.get_attribute('href') if link_elem else None
            
            # Extract details from vehicle details section
            details_items = listing_element.query_selector_all('[data-testid="vehicle-summary-item"]')
            
            for item in details_items:
                text = item.inner_text().strip()
                
                # Mileage (km)
                if 'km' in text.lower():
                    data['mileage'] = self._parse_mileage(text)
                
                # Registration/Year
                elif '/' in text and len(text) <= 7:  # e.g., "12/2020"
                    data['year'] = self._parse_year(text)
                
                # Power (kW/HP)
                elif 'kw' in text.lower() or 'ps' in text.lower():
                    data['horsepower'] = self._parse_power(text)
                
                # Fuel type
                elif any(fuel in text.lower() for fuel in ['benzin', 'diesel', 'elektro', 'hybrid']):
                    data['fuel_type'] = text
                
                # Transmission
                elif any(trans in text.lower() for trans in ['automatik', 'schaltgetriebe', 'manuell']):
                    data['transmission'] = text
            
            # Extract location
            location_elem = listing_element.query_selector('[data-testid="seller-location"]')
            data['location'] = location_elem.inner_text().strip() if location_elem else None
            
            # Set condition based on URL or damage indicator
            data['condition'] = 'damaged' if 'damaged' in str(data.get('url', '')) else 'functional'
            
            # Set site source
            data['source'] = 'AutoScout24'
            
        except Exception as e:
            logger.warning(f"Error extracting listing data: {e}")
        
        return data
    
    def has_next_page(self, page: Page) -> bool:
        """
        Check if there is a next page of results.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if next page exists, False otherwise
        """
        try:
            next_button = page.query_selector('a[data-testid="pagination-next"]')
            if next_button:
                # Check if button is disabled
                is_disabled = next_button.get_attribute('aria-disabled') == 'true'
                return not is_disabled
            return False
        except Exception as e:
            logger.warning(f"Error checking for next page: {e}")
            return False
    
    def go_to_next_page(self, page: Page) -> bool:
        """
        Navigate to the next page of results.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            next_button = page.query_selector('a[data-testid="pagination-next"]')
            if next_button:
                next_button.click()
                page.wait_for_load_state('domcontentloaded')
                return True
            return False
        except Exception as e:
            logger.warning(f"Error navigating to next page: {e}")
            return False
    
    @staticmethod
    def _parse_price(price_text: str) -> Optional[float]:
        """Parse price from text."""
        try:
            # Remove currency symbols and spaces, extract numbers
            price_str = re.sub(r'[^\d,]', '', price_text)
            price_str = price_str.replace(',', '.')
            return float(price_str) if price_str else None
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def _parse_mileage(mileage_text: str) -> Optional[int]:
        """Parse mileage from text."""
        try:
            # Extract numbers before 'km'
            match = re.search(r'([\d.]+)', mileage_text.replace('.', ''))
            return int(match.group(1)) if match else None
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def _parse_year(year_text: str) -> Optional[int]:
        """Parse year from registration date."""
        try:
            # Extract year from format like "12/2020"
            match = re.search(r'/(\d{4})', year_text)
            if match:
                return int(match.group(1))
            # Try just 4-digit year
            match = re.search(r'(\d{4})', year_text)
            return int(match.group(1)) if match else None
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def _parse_power(power_text: str) -> Optional[int]:
        """Parse horsepower from text."""
        try:
            # Look for HP (PS) value
            match = re.search(r'(\d+)\s*PS', power_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
            # Look for kW value and convert to HP
            match = re.search(r'(\d+)\s*kW', power_text, re.IGNORECASE)
            if match:
                kw = int(match.group(1))
                return int(kw * 1.36)  # Convert kW to HP
            return None
        except (ValueError, AttributeError):
            return None
