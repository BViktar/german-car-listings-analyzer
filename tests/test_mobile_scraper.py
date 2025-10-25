"""Unit tests for Mobile.de scraper."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import requests

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper.mobile_scraper import MobileDeScraper


class TestMobileDeScraper(unittest.TestCase):
    """Test cases for MobileDeScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = MobileDeScraper()
        
    def test_init(self):
        """Test scraper initialization."""
        self.assertIsNotNone(self.scraper)
        self.assertEqual(self.scraper.BASE_URL, "https://www.mobile.de")
        self.assertIsNotNone(self.scraper.logger)
        
    def test_search_broken_motors_params(self):
        """Test that search_broken_motors uses correct parameters."""
        with patch.object(self.scraper, '_search_listings') as mock_search:
            mock_search.return_value = []
            self.scraper.search_broken_motors()
            
            # Verify the method was called with correct params
            self.assertTrue(mock_search.called)
            params = mock_search.call_args[0][0]
            self.assertEqual(params['damageUnrepaired'], 'BRAND_OR_MECHANICAL_DAMAGE')
            self.assertEqual(params['countryCode'], 'DE')
            
    def test_search_functional_cars_params(self):
        """Test that search_functional_cars uses correct parameters."""
        with patch.object(self.scraper, '_search_listings') as mock_search:
            mock_search.return_value = []
            min_price = 15000
            self.scraper.search_functional_cars(min_price=min_price)
            
            # Verify the method was called with correct params
            self.assertTrue(mock_search.called)
            params = mock_search.call_args[0][0]
            self.assertEqual(params['minPrice'], str(min_price))
            self.assertEqual(params['damageUnrepaired'], 'NO_DAMAGE')
            
    def test_extract_number(self):
        """Test number extraction from various formats."""
        # Test with currency symbols
        self.assertEqual(self.scraper._extract_number("€15,000"), 15000)
        self.assertEqual(self.scraper._extract_number("$25.000"), 25000)
        
        # Test with spaces
        self.assertEqual(self.scraper._extract_number("100 000 km"), 100000)
        
        # Test with plain numbers
        self.assertEqual(self.scraper._extract_number("12345"), 12345)
        
        # Test with no numbers
        self.assertIsNone(self.scraper._extract_number("No price"))
        
    def test_extract_listing_data(self):
        """Test extraction of listing data from HTML element."""
        html = """
        <div class="listing-item">
            <h2 class="vehicle-data--title">BMW 320d</h2>
            <a href="/auto/bmw-320d-12345">View</a>
            <span class="price">€15,000</span>
            <span data-testid="mileage">100,000 km</span>
            <span data-testid="first-registration">2018</span>
            <span data-testid="fuel-type">Diesel</span>
            <span data-testid="transmission">Automatic</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='listing-item')
        
        data = self.scraper._extract_listing_data(element)
        
        self.assertEqual(data['title'], 'BMW 320d')
        self.assertEqual(data['make'], 'BMW')
        self.assertEqual(data['model'], '320d')
        self.assertEqual(data['price'], 15000)
        self.assertEqual(data['mileage'], 100000)
        self.assertEqual(data['year'], 2018)
        self.assertEqual(data['fuel_type'], 'Diesel')
        self.assertEqual(data['transmission'], 'Automatic')
        self.assertTrue(data['url'].endswith('/auto/bmw-320d-12345'))
        
    def test_parse_listings_with_elements(self):
        """Test parsing of multiple listings."""
        html = """
        <div>
            <div class="cBox-body--resultitem">
                <h2 class="vehicle-data--title">Audi A4</h2>
                <a href="/auto/audi-a4-1">View</a>
                <span class="price">€20,000</span>
            </div>
            <div class="cBox-body--resultitem">
                <h2 class="vehicle-data--title">Mercedes C200</h2>
                <a href="/auto/mercedes-c200-2">View</a>
                <span class="price">€25,000</span>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        listings = self.scraper._parse_listings(soup)
        
        self.assertEqual(len(listings), 2)
        self.assertEqual(listings[0]['title'], 'Audi A4')
        self.assertEqual(listings[1]['title'], 'Mercedes C200')
        
    def test_parse_listings_empty(self):
        """Test parsing with no listings found."""
        html = "<div><p>No results</p></div>"
        soup = BeautifulSoup(html, 'html.parser')
        
        listings = self.scraper._parse_listings(soup)
        
        self.assertEqual(len(listings), 0)
        
    @patch('src.scraper.mobile_scraper.requests.Session')
    def test_search_listings_network_error(self, mock_session_class):
        """Test handling of network errors."""
        # Setup mock to raise RequestException
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_session.get.side_effect = requests.RequestException("Network error")
        
        scraper = MobileDeScraper()
        result = scraper._search_listings({})
        
        # Should return empty list on error
        self.assertEqual(result, [])
        
    def test_parse_json_ld(self):
        """Test parsing of JSON-LD structured data."""
        html = """
        <script type="application/ld+json">
        {
            "@type": "Car",
            "name": "VW Golf",
            "brand": {"name": "Volkswagen"},
            "model": "Golf",
            "productionDate": "2020",
            "mileageFromOdometer": {"value": "50000"},
            "offers": {"price": "18000"},
            "fuelType": "Benzin",
            "vehicleTransmission": "Manual",
            "url": "https://www.mobile.de/auto/vw-golf"
        }
        </script>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        listings = self.scraper._parse_json_ld(soup)
        
        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0]['title'], 'VW Golf')
        self.assertEqual(listings[0]['make'], 'Volkswagen')
        self.assertEqual(listings[0]['year'], '2020')
        
    def test_extract_listing_data_partial_info(self):
        """Test extraction with partial information."""
        html = """
        <div class="listing-item">
            <h2 class="vehicle-data--title">Ford Focus</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='listing-item')
        
        data = self.scraper._extract_listing_data(element)
        
        # Should have title but other fields should be empty/None
        self.assertEqual(data['title'], 'Ford Focus')
        self.assertEqual(data['make'], 'Ford')
        self.assertEqual(data['model'], 'Focus')
        self.assertIsNone(data['price'])
        self.assertIsNone(data['mileage'])
        
    def test_extract_year_from_text(self):
        """Test year extraction from various text formats."""
        html = """
        <div class="listing-item">
            <h2 class="vehicle-data--title">Test Car</h2>
            <span>First registration: 03/2019</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='listing-item')
        
        data = self.scraper._extract_listing_data(element)
        
        self.assertEqual(data['year'], 2019)


class TestBaseScraper(unittest.TestCase):
    """Test cases for BaseScraper functionality."""
    
    def test_rate_limiting(self):
        """Test that rate limiting is enforced."""
        import time
        scraper = MobileDeScraper()
        scraper.rate_limit = 0.5  # 0.5 seconds between requests
        
        # Mock the session.get to avoid actual network calls
        with patch.object(scraper.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.text = "<html></html>"
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            start_time = time.time()
            scraper._make_request("https://example.com")
            scraper._make_request("https://example.com")
            elapsed_time = time.time() - start_time
            
            # Should have waited at least the rate limit time
            self.assertGreaterEqual(elapsed_time, 0.5)
            
    def test_session_headers(self):
        """Test that session has proper headers set."""
        scraper = MobileDeScraper()
        
        self.assertIn('User-Agent', scraper.session.headers)
        self.assertIn('Accept', scraper.session.headers)
        self.assertIn('Mozilla', scraper.session.headers['User-Agent'])


if __name__ == '__main__':
    unittest.main()
