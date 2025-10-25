"""Mobile.de scraper implementation."""

import logging
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlencode
from playwright.sync_api import Page

from src.scraper.base_scraper import BaseScraper
from src.config import MOBILE_DE_SEARCH_URL

logger = logging.getLogger(__name__)


class MobileDeScraper(BaseScraper):
    """
    Scraper for Mobile.de car listings.
    
    Implements site-specific parsing and data extraction logic for Mobile.de.
    """
    
    def get_site_name(self) -> str:
        """Get the name of the website being scraped."""
        return "Mobile.de"
    
    def build_search_url(self, **kwargs) -> str:
        """
        Build the search URL for Mobile.de.
        
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
            params['makeModelVariant1.makeId'] = kwargs['make']
        if kwargs.get('model'):
            params['makeModelVariant1.modelId'] = kwargs['model']
        
        # Add year range
        if kwargs.get('year_min'):
            params['minFirstRegistrationDate'] = kwargs['year_min']
        if kwargs.get('year_max'):
            params['maxFirstRegistrationDate'] = kwargs['year_max']
        
        # Add mileage
        if kwargs.get('mileage_max'):
            params['maxMileage'] = kwargs['mileage_max']
        
        # Add damaged filter
        if kwargs.get('damaged', False):
            params['dam'] = 'true'
        
        # Add default sorting
        params['sorting'] = 'creationTime_desc'
        
        query_string = urlencode(params) if params else ''
        url = f"{MOBILE_DE_SEARCH_URL}?{query_string}" if query_string else MOBILE_DE_SEARCH_URL
        
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
            page.wait_for_selector('[data-testid="result-list-item"]', 
                                  timeout=10000, state='visible')
            
            # Get all listing elements
            elements = page.query_selector_all('[data-testid="result-list-item"]')
            return elements
        except Exception as e:
            logger.warning(f"Could not find listing elements: {e}")
            return []
    
    def extract_listing_data(self, page: Page, listing_element: Any) -> Dict[str, Any]:
        """
        Extract data from a single Mobile.de listing element.
        
        Args:
            page: Playwright page object
            listing_element: Listing element to extract data from
            
        Returns:
            Dictionary containing extracted listing data
        """
        data: Dict[str, Any] = {}
        
        try:
            # Extract title
            title_elem = listing_element.query_selector('[data-testid="result-list-item-title"]')
            data['title'] = title_elem.inner_text().strip() if title_elem else None
            
            # Extract price
            price_elem = listing_element.query_selector('[data-testid="prime-price"]')
            if price_elem:
                price_text = price_elem.inner_text().strip()
                data['price'] = self._parse_price(price_text)
            else:
                data['price'] = None
            
            # Extract URL
            link_elem = listing_element.query_selector('a[href*="/details/"]')
            data['url'] = link_elem.get_attribute('href') if link_elem else None
            
            # Extract vehicle details
            details_elem = listing_element.query_selector('[data-testid="result-list-item-details"]')
            if details_elem:
                details_text = details_elem.inner_text()
                
                # Parse mileage
                mileage_match = re.search(r'([\d.]+)\s*km', details_text)
                if mileage_match:
                    data['mileage'] = self._parse_mileage(mileage_match.group(0))
                
                # Parse year
                year_match = re.search(r'(\d{2})/(\d{4})', details_text)
                if year_match:
                    data['year'] = int(year_match.group(2))
                
                # Parse power
                power_match = re.search(r'(\d+)\s*kW\s*\((\d+)\s*PS\)', details_text)
                if power_match:
                    data['horsepower'] = int(power_match.group(2))
                
                # Parse fuel type
                fuel_types = ['Benzin', 'Diesel', 'Elektro', 'Hybrid', 'Autogas', 'Erdgas']
                for fuel in fuel_types:
                    if fuel.lower() in details_text.lower():
                        data['fuel_type'] = fuel
                        break
                
                # Parse transmission
                if 'Automatik' in details_text:
                    data['transmission'] = 'Automatik'
                elif 'Schaltgetriebe' in details_text or 'Manuell' in details_text:
                    data['transmission'] = 'Schaltgetriebe'
            
            # Extract location
            location_elem = listing_element.query_selector('[data-testid="result-list-item-location"]')
            data['location'] = location_elem.inner_text().strip() if location_elem else None
            
            # Extract seller type
            seller_elem = listing_element.query_selector('[data-testid="result-list-item-seller-type"]')
            data['seller_type'] = seller_elem.inner_text().strip() if seller_elem else None
            
            # Check for damage indicator
            damage_badge = listing_element.query_selector('[data-testid="damage-badge"]')
            data['condition'] = 'damaged' if damage_badge else 'functional'
            
            # Set site source
            data['source'] = 'Mobile.de'
            
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
            next_button = page.query_selector('[data-testid="pagination-next"]')
            if next_button:
                # Check if button is disabled
                is_disabled = next_button.get_attribute('disabled') is not None
                aria_disabled = next_button.get_attribute('aria-disabled') == 'true'
                return not (is_disabled or aria_disabled)
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
            next_button = page.query_selector('[data-testid="pagination-next"]')
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
            price_str = price_str.replace('.', '').replace(',', '.')
            return float(price_str) if price_str else None
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def _parse_mileage(mileage_text: str) -> Optional[int]:
        """Parse mileage from text."""
        try:
            # Extract numbers before 'km', remove dots
            match = re.search(r'([\d.]+)', mileage_text)
            if match:
                mileage_str = match.group(1).replace('.', '')
                return int(mileage_str)
            return None
        except (ValueError, AttributeError):
            return None
