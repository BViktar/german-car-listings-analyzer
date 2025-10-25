"""Mobile.de scraper implementation."""

from typing import Dict, List
import logging
import requests
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class MobileScraper(BaseScraper):
    """Scraper for Mobile.de German car listing website."""
    
    BASE_URL = "https://www.mobile.de"
    
    def __init__(self):
        """Initialize Mobile.de scraper with session."""
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def search_broken_motors(self) -> List[Dict]:
        """Search for cars with broken motors on Mobile.de.
        
        Returns:
            List[Dict]: List of car listings with broken motors.
            Each dictionary contains car details like make, model, price, etc.
        """
        self.logger.info("Searching for broken motor cars on Mobile.de")
        results = []
        
        try:
            # Mobile.de search parameters for damaged/non-running vehicles
            search_params = {
                'dam': 'true',  # damaged cars
                's': 'Price',   # sort by price
                'sb': 'asc',    # ascending
            }
            
            search_url = f"{self.BASE_URL}/search"
            
            # Add random user agent
            self.session.headers.update({
                'User-Agent': self._get_random_user_agent()
            })
            
            self.logger.debug(f"Fetching: {search_url} with params: {search_params}")
            response = self.session.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            
            # Parse response
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = self._parse_listings(soup, broken_motor=True)
            results.extend(listings)
            
            self.logger.info(f"Found {len(results)} broken motor listings")
            
            # Implement delay before next request
            self._implement_delay()
            
        except requests.RequestException as e:
            self._handle_request_error(e, search_url)
        except Exception as e:
            self.logger.error(f"Unexpected error in search_broken_motors: {str(e)}", exc_info=True)
            
        return results
        
    def search_functional_cars(self, min_price: int = 10000) -> List[Dict]:
        """Search for functional cars above minimum price on Mobile.de.
        
        Args:
            min_price: Minimum price threshold in EUR (default: 10000).
            
        Returns:
            List[Dict]: List of functional car listings above the minimum price.
        """
        self.logger.info(f"Searching for functional cars on Mobile.de with min price: €{min_price}")
        results = []
        
        try:
            # Search parameters for functional cars above minimum price
            search_params = {
                'p': str(min_price),  # price from
                's': 'Price',         # sort by price
                'sb': 'asc',          # ascending
                'dam': 'false',       # not damaged
            }
            
            search_url = f"{self.BASE_URL}/search"
            
            # Add random user agent
            self.session.headers.update({
                'User-Agent': self._get_random_user_agent()
            })
            
            self.logger.debug(f"Fetching: {search_url} with params: {search_params}")
            response = self.session.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            
            # Parse response
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = self._parse_listings(soup, broken_motor=False)
            results.extend(listings)
            
            self.logger.info(f"Found {len(results)} functional car listings")
            
            # Implement delay before next request
            self._implement_delay()
            
        except requests.RequestException as e:
            self._handle_request_error(e, search_url)
        except Exception as e:
            self.logger.error(f"Unexpected error in search_functional_cars: {str(e)}", exc_info=True)
            
        return results
        
    def _parse_listings(self, soup: BeautifulSoup, broken_motor: bool = False) -> List[Dict]:
        """Parse car listings from Mobile.de HTML.
        
        Args:
            soup: BeautifulSoup object containing the page HTML.
            broken_motor: Whether these are broken motor listings.
            
        Returns:
            List[Dict]: Parsed car listing data.
        """
        listings = []
        
        try:
            # Find all listing containers (Mobile.de structure)
            # Note: This is a simplified parser - actual site structure may vary
            listing_elements = soup.find_all('div', class_='cBox-body--resultitem')
            
            if not listing_elements:
                # Try alternative selectors
                listing_elements = soup.find_all('div', {'data-ad-id': True})
            
            self.logger.debug(f"Found {len(listing_elements)} listing elements")
            
            for listing_elem in listing_elements:
                try:
                    listing_data = {
                        'source': 'Mobile.de',
                        'broken_motor': broken_motor,
                    }
                    
                    # Extract title/make/model
                    title_elem = listing_elem.find('span', class_='h3') or listing_elem.find('div', class_='vehicle-data')
                    if title_elem:
                        listing_data['title'] = title_elem.get_text(strip=True)
                    
                    # Extract price
                    price_elem = listing_elem.find('span', class_='price-label') or listing_elem.find('div', class_='price')
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        listing_data['price_text'] = price_text
                        # Try to extract numeric price
                        try:
                            price_num = ''.join(filter(str.isdigit, price_text))
                            if price_num:
                                listing_data['price'] = int(price_num)
                        except ValueError:
                            pass
                    
                    # Extract mileage
                    mileage_elem = listing_elem.find('span', class_='mileage')
                    if not mileage_elem:
                        # Try to find in vehicle data
                        vehicle_data = listing_elem.find('div', class_='vehicle-data')
                        if vehicle_data:
                            mileage_text = vehicle_data.find(string=lambda x: x and 'km' in x.lower())
                            if mileage_text:
                                listing_data['mileage'] = mileage_text.strip()
                    else:
                        listing_data['mileage'] = mileage_elem.get_text(strip=True)
                    
                    # Extract year
                    year_elem = listing_elem.find('span', class_='year')
                    if year_elem:
                        listing_data['year'] = year_elem.get_text(strip=True)
                    
                    # Extract link
                    link_elem = listing_elem.find('a', class_='link--detail') or listing_elem.find('a', href=True)
                    if link_elem:
                        href = link_elem.get('href', '')
                        if href:
                            if href.startswith('/'):
                                href = self.BASE_URL + href
                            listing_data['url'] = href
                    
                    # Extract location
                    location_elem = listing_elem.find('span', class_='seller-info__location')
                    if location_elem:
                        listing_data['location'] = location_elem.get_text(strip=True)
                    
                    # Only add if we have at least title or price
                    if 'title' in listing_data or 'price' in listing_data:
                        listings.append(listing_data)
                        
                except Exception as e:
                    self.logger.warning(f"Error parsing individual listing: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing listings: {str(e)}", exc_info=True)
            
        return listings
