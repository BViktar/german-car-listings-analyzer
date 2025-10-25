"""AutoScout24 scraper implementation."""
from typing import Dict, List, Optional
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import logging
import json
import re


class AutoScout24Scraper(BaseScraper):
    """Scraper for AutoScout24.de car listings."""
    
    BASE_URL = "https://www.autoscout24.de"
    SEARCH_URL = f"{BASE_URL}/lst"
    
    def __init__(self):
        """Initialize AutoScout24 scraper with specific settings."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        # Increase delay for AutoScout24 to avoid rate limiting
        self.request_delay = 3
        
    def search_broken_motors(self) -> List[Dict]:
        """
        Search for cars with broken motors ("Motorschaden").
        
        Returns:
            List of dictionaries containing listing data
        """
        self.logger.info("Searching for cars with broken motors (Motorschaden)")
        params = {
            'desc': '0',  # Sort descending
            'cy': 'D',    # Germany only
            'atype': 'C',  # Cars only
            'ustate': 'N',  # New listings first
            'damaged': '1',  # Include damaged vehicles
            'keyword': 'Motorschaden'  # Search for "Motorschaden"
        }
        return self._search_listings(params)
        
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """
        Search for functional cars above minimum price.
        
        Args:
            min_price: Minimum price threshold in euros (default: 10000)
            
        Returns:
            List of dictionaries containing listing data
        """
        self.logger.info(f"Searching for functional cars with min price {min_price}")
        params = {
            'desc': '0',
            'cy': 'D',
            'atype': 'C',
            'ustate': 'N',
            'damaged': '0',  # Exclude damaged vehicles
            'pricefrom': str(min_price)
        }
        return self._search_listings(params)
        
    def _search_listings(self, params: Dict) -> List[Dict]:
        """
        Execute search and parse results.
        
        Args:
            params: Dictionary of search parameters
            
        Returns:
            List of parsed listing dictionaries
        """
        listings = []
        try:
            response = self._make_request(self.SEARCH_URL, params)
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = self._parse_listings(soup)
            self.logger.info(f"Successfully parsed {len(listings)} listings")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error searching listings: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error searching listings: {str(e)}", exc_info=True)
        return listings
        
    def _parse_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse individual listing data from search results.
        
        AutoScout24 uses various HTML structures depending on the page layout.
        This method attempts to find listings using common selectors.
        
        Args:
            soup: BeautifulSoup object of the search results page
            
        Returns:
            List of parsed listing dictionaries
        """
        listings = []
        
        # Try multiple selectors as AutoScout24's structure can vary
        # Common selectors for listing items
        selectors = [
            'article[data-item-name="listing-summary-vehicles"]',
            'article.cldt-summary-full-item',
            'div.cl-list-element',
            'article.ListItem_article__ppZSb',
            'div[data-testid="listing-summary"]'
        ]
        
        listing_elements = []
        for selector in selectors:
            listing_elements = soup.select(selector)
            if listing_elements:
                self.logger.debug(f"Found {len(listing_elements)} listings using selector: {selector}")
                break
        
        if not listing_elements:
            self.logger.warning("No listing elements found on page")
            # Try to find any articles or divs that might contain listings
            listing_elements = soup.find_all('article')
            if not listing_elements:
                listing_elements = soup.find_all('div', class_=re.compile(r'ListItem|listing|vehicle', re.I))
            
        for element in listing_elements:
            try:
                listing_data = self._extract_listing_data(element)
                # Only add if we extracted meaningful data
                if listing_data.get('title') or listing_data.get('price'):
                    listings.append(listing_data)
            except Exception as e:
                self.logger.debug(f"Error parsing individual listing: {str(e)}")
                continue
                
        return listings
        
    def _extract_listing_data(self, listing_element) -> Dict:
        """
        Extract data from a single listing element.
        
        Args:
            listing_element: BeautifulSoup element containing a single listing
            
        Returns:
            Dictionary with extracted listing data
        """
        data = {
            'title': '',
            'make': '',
            'model': '',
            'year': None,
            'mileage': None,
            'price': None,
            'fuel_type': '',
            'transmission': '',
            'url': '',
            'location': '',
            'seller_type': ''
        }
        
        try:
            # Extract title
            title_selectors = [
                'h2',
                'h3',
                '[data-testid="listing-title"]',
                '.cldt-summary-makemodel',
                '.ListItem_title__ndA4c'
            ]
            for selector in title_selectors:
                title_elem = listing_element.select_one(selector)
                if title_elem:
                    data['title'] = title_elem.get_text(strip=True)
                    break
            
            # Try to extract make and model from title
            if data['title']:
                parts = data['title'].split()
                if len(parts) >= 2:
                    data['make'] = parts[0]
                    data['model'] = ' '.join(parts[1:])
            
            # Extract URL
            link_elem = listing_element.find('a', href=True)
            if link_elem:
                url = link_elem['href']
                if url.startswith('/'):
                    url = self.BASE_URL + url
                data['url'] = url
            
            # Extract price
            price_selectors = [
                '[data-testid="listing-price"]',
                '.cldt-price',
                '.Price_price__XGxpT',
                'span.sc-font-bold.sc-font-xl'
            ]
            for selector in price_selectors:
                price_elem = listing_element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric value from price
                    price_match = re.search(r'([\d.]+)', price_text.replace('.', '').replace(',', ''))
                    if price_match:
                        try:
                            data['price'] = int(price_match.group(1))
                        except ValueError:
                            pass
                    break
            
            # Extract vehicle details (mileage, year, fuel type, transmission)
            # These are often in a list of details
            detail_selectors = [
                'ul li',
                'span[class*="VehicleDetailTable"]',
                '.cldt-summary-detail',
                'div[data-testid="listing-detail"]'
            ]
            
            details_text = []
            for selector in detail_selectors:
                details = listing_element.select(selector)
                if details:
                    details_text = [d.get_text(strip=True) for d in details]
                    break
            
            # Parse details
            for detail in details_text:
                detail_lower = detail.lower()
                
                # Mileage (km)
                if 'km' in detail_lower:
                    km_match = re.search(r'([\d.]+)', detail.replace('.', '').replace(',', ''))
                    if km_match:
                        try:
                            data['mileage'] = int(km_match.group(1))
                        except ValueError:
                            pass
                
                # Year
                year_match = re.search(r'\b(19|20)\d{2}\b', detail)
                if year_match:
                    try:
                        data['year'] = int(year_match.group(0))
                    except ValueError:
                        pass
                
                # Fuel type
                fuel_types = ['benzin', 'diesel', 'elektro', 'hybrid', 'gas', 'lpg', 'cng']
                for fuel in fuel_types:
                    if fuel in detail_lower:
                        data['fuel_type'] = fuel.capitalize()
                        break
                
                # Transmission
                if 'automatik' in detail_lower or 'automatic' in detail_lower:
                    data['transmission'] = 'Automatic'
                elif 'schaltgetriebe' in detail_lower or 'manuell' in detail_lower or 'manual' in detail_lower:
                    data['transmission'] = 'Manual'
            
            # Extract location
            location_selectors = [
                '[data-testid="listing-location"]',
                '.cldt-summary-dealer-contact-city',
                '.listing-location'
            ]
            for selector in location_selectors:
                location_elem = listing_element.select_one(selector)
                if location_elem:
                    data['location'] = location_elem.get_text(strip=True)
                    break
            
        except Exception as e:
            self.logger.debug(f"Error extracting listing data: {str(e)}")
        
        return data
