"""Mobile.de scraper implementation for car listings."""

from typing import Dict, List, Optional
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import logging
import json
import re


class MobileDeScraper(BaseScraper):
    """Scraper for Mobile.de car listings."""
    
    BASE_URL = "https://www.mobile.de"
    SEARCH_URL = f"{BASE_URL}/auto"
    
    def __init__(self):
        """Initialize the Mobile.de scraper."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
    def search_broken_motors(self) -> List[Dict]:
        """
        Search for cars with broken motors ("Motorschaden").
        
        Returns:
            List of car listings with broken motors
        """
        params = {
            'damageUnrepaired': 'BRAND_OR_MECHANICAL_DAMAGE',  # Mobile.de specific parameter
            'isSearchRequest': 'true',
            'scopeId': 'C',  # Cars
            'sfmr': 'false',  # No radius search
            'categories': 'Car',
            'sortOption.sortBy': 'creationTime',
            'sortOption.sortOrder': 'DESCENDING',
            'lang': 'en',
            'countryCode': 'DE'  # Germany only
        }
        return self._search_listings(params)
        
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """
        Search for functional cars above minimum price.
        
        Args:
            min_price: Minimum price threshold (default: 10000)
            
        Returns:
            List of functional car listings
        """
        params = {
            'isSearchRequest': 'true',
            'scopeId': 'C',
            'sfmr': 'false',
            'categories': 'Car',
            'minPrice': str(min_price),
            'damageUnrepaired': 'NO_DAMAGE',  # Exclude damaged cars
            'sortOption.sortBy': 'price',
            'sortOption.sortOrder': 'ASCENDING',
            'lang': 'en',
            'countryCode': 'DE'
        }
        return self._search_listings(params)
        
    def _search_listings(self, params: Dict) -> List[Dict]:
        """
        Execute search and parse results.
        
        Args:
            params: Search parameters for Mobile.de API
            
        Returns:
            List of parsed car listings
        """
        listings = []
        try:
            response = self._make_request(self.SEARCH_URL, params)
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = self._parse_listings(soup)
            self.logger.info(f"Successfully parsed {len(listings)} listings")
        except requests.RequestException as e:
            self.logger.error(f"Network error searching listings: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error searching listings: {str(e)}", exc_info=True)
        return listings
        
    def _parse_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse individual listing data from search results.
        
        Mobile.de uses various CSS classes for listing containers. This method
        attempts to find listings using common selectors.
        
        Args:
            soup: BeautifulSoup object of the search results page
            
        Returns:
            List of parsed car listings
        """
        listings = []
        
        try:
            # Try multiple possible selectors for listing elements
            # Mobile.de may use different class names or structure
            listing_selectors = [
                'div.cBox-body--resultitem',
                'div[data-listing-id]',
                'article.listing-item',
                'div.vehicle-data',
                'div.result-item',
                'div.cBox.cBox--resultList'
            ]
            
            listing_elements = []
            for selector in listing_selectors:
                listing_elements = soup.select(selector)
                if listing_elements:
                    self.logger.debug(f"Found {len(listing_elements)} elements with selector: {selector}")
                    break
            
            if not listing_elements:
                self.logger.warning("No listing elements found on page")
                # Try to extract JSON-LD structured data as fallback
                listings = self._parse_json_ld(soup)
                if listings:
                    return listings
            
            for element in listing_elements:
                try:
                    listing_data = self._extract_listing_data(element)
                    if listing_data and listing_data.get('title'):
                        listings.append(listing_data)
                except Exception as e:
                    self.logger.warning(f"Failed to parse individual listing: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing listings: {str(e)}", exc_info=True)
            
        return listings
        
    def _parse_json_ld(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse JSON-LD structured data from the page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of parsed listings from JSON-LD data
        """
        listings = []
        try:
            # Look for JSON-LD script tags
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    # Check if it's a product or item list
                    if isinstance(data, dict) and data.get('@type') in ['Product', 'Car', 'Vehicle']:
                        listing = self._extract_from_json_ld(data)
                        if listing:
                            listings.append(listing)
                    elif isinstance(data, dict) and data.get('@type') == 'ItemList':
                        items = data.get('itemListElement', [])
                        for item in items:
                            listing = self._extract_from_json_ld(item)
                            if listing:
                                listings.append(listing)
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            self.logger.debug(f"Failed to parse JSON-LD: {str(e)}")
        
        return listings
        
    def _extract_from_json_ld(self, data: Dict) -> Optional[Dict]:
        """
        Extract listing data from JSON-LD structured data.
        
        Args:
            data: JSON-LD data object
            
        Returns:
            Parsed listing dictionary or None
        """
        try:
            # Extract brand name, handling both dict and string formats
            brand = data.get('brand', {})
            make = brand.get('name', '') if isinstance(brand, dict) else ''
            
            return {
                'title': data.get('name', ''),
                'make': make,
                'model': data.get('model', ''),
                'year': data.get('productionDate', data.get('modelDate')),
                'mileage': self._extract_number(str(data.get('mileageFromOdometer', {}).get('value', ''))),
                'price': self._extract_number(str(data.get('offers', {}).get('price', ''))),
                'fuel_type': data.get('fuelType', ''),
                'transmission': data.get('vehicleTransmission', ''),
                'url': data.get('url', '')
            }
        except Exception as e:
            self.logger.debug(f"Failed to extract from JSON-LD: {str(e)}")
            return None
        
    def _extract_listing_data(self, listing_element) -> Dict:
        """
        Extract data from a single listing element.
        
        Args:
            listing_element: BeautifulSoup element representing a single listing
            
        Returns:
            Dictionary containing extracted listing data
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
            'url': ''
        }
        
        try:
            # Extract title
            title_elem = (
                listing_element.select_one('h2.vehicle-data--title') or
                listing_element.select_one('div.h2') or
                listing_element.select_one('[data-testid="result-title"]') or
                listing_element.select_one('a.link--primary')
            )
            if title_elem:
                data['title'] = title_elem.get_text(strip=True)
                # Parse make and model from title
                parts = data['title'].split()
                if len(parts) >= 2:
                    data['make'] = parts[0]
                    data['model'] = parts[1]
            
            # Extract URL
            link_elem = listing_element.select_one('a[href*="/auto/"]')
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                data['url'] = href if href.startswith('http') else f"{self.BASE_URL}{href}"
            
            # Extract price
            price_elem = (
                listing_element.select_one('span.price') or
                listing_element.select_one('[data-testid="price"]') or
                listing_element.select_one('div.price-block')
            )
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                data['price'] = self._extract_number(price_text)
            
            # Extract mileage
            mileage_elem = (
                listing_element.select_one('span[data-testid="mileage"]') or
                listing_element.find(string=re.compile(r'\d+\s*km', re.IGNORECASE))
            )
            if mileage_elem:
                mileage_text = mileage_elem if isinstance(mileage_elem, str) else mileage_elem.get_text(strip=True)
                data['mileage'] = self._extract_number(mileage_text)
            
            # Extract year
            year_elem = (
                listing_element.select_one('span[data-testid="first-registration"]') or
                listing_element.find(string=re.compile(r'\b(19|20)\d{2}\b'))
            )
            if year_elem:
                year_text = year_elem if isinstance(year_elem, str) else year_elem.get_text(strip=True)
                year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                if year_match:
                    data['year'] = int(year_match.group())
            
            # Extract fuel type
            fuel_elem = listing_element.select_one('span[data-testid="fuel-type"]')
            if fuel_elem:
                data['fuel_type'] = fuel_elem.get_text(strip=True)
            else:
                # Try to find in vehicle details
                details = listing_element.get_text()
                fuel_types = ['Benzin', 'Diesel', 'Elektro', 'Hybrid', 'Gasoline', 'Electric']
                for fuel in fuel_types:
                    if fuel.lower() in details.lower():
                        data['fuel_type'] = fuel
                        break
            
            # Extract transmission
            trans_elem = listing_element.select_one('span[data-testid="transmission"]')
            if trans_elem:
                data['transmission'] = trans_elem.get_text(strip=True)
            else:
                # Try to find in vehicle details
                details = listing_element.get_text()
                if 'automatik' in details.lower() or 'automatic' in details.lower():
                    data['transmission'] = 'Automatic'
                elif 'schaltgetriebe' in details.lower() or 'manual' in details.lower():
                    data['transmission'] = 'Manual'
                    
        except Exception as e:
            self.logger.warning(f"Error extracting listing data: {str(e)}")
            
        return data
        
    def _extract_number(self, text: str) -> Optional[int]:
        """
        Extract numeric value from text string.
        
        Handles common European number formats with dots and commas as separators.
        Note: This extracts integers only and removes all separators.
        
        Args:
            text: Text containing a number
            
        Returns:
            Extracted integer value or None
        """
        try:
            # Remove currency symbols and common separators (dots, commas, spaces)
            # This works for formats like: €15,000, 100.000 km, $25,000
            cleaned = re.sub(r'[€$,.\s]', '', text)
            # Extract first sequence of digits
            match = re.search(r'\d+', cleaned)
            if match:
                return int(match.group())
        except (ValueError, AttributeError):
            pass
        return None
