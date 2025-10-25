"""Tests for AutoScout24 scraper implementation."""
import unittest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper.autoscout_scraper import AutoScout24Scraper
from scraper.base_scraper import BaseScraper


class TestAutoScout24Scraper(unittest.TestCase):
    """Test cases for AutoScout24Scraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = AutoScout24Scraper()
    
    def test_init(self):
        """Test scraper initialization."""
        self.assertIsInstance(self.scraper, AutoScout24Scraper)
        self.assertIsInstance(self.scraper, BaseScraper)
        self.assertEqual(self.scraper.BASE_URL, "https://www.autoscout24.de")
        self.assertEqual(self.scraper.request_delay, 3)
    
    def test_search_broken_motors_params(self):
        """Test that search_broken_motors generates correct parameters."""
        with patch.object(self.scraper, '_search_listings') as mock_search:
            mock_search.return_value = []
            self.scraper.search_broken_motors()
            
            # Check that _search_listings was called with correct params
            mock_search.assert_called_once()
            params = mock_search.call_args[0][0]
            self.assertEqual(params['damaged'], '1')
            self.assertEqual(params['keyword'], 'Motorschaden')
            self.assertEqual(params['cy'], 'D')
            self.assertEqual(params['atype'], 'C')
    
    def test_search_functional_cars_params(self):
        """Test that search_functional_cars generates correct parameters."""
        with patch.object(self.scraper, '_search_listings') as mock_search:
            mock_search.return_value = []
            self.scraper.search_functional_cars(min_price=15000)
            
            # Check that _search_listings was called with correct params
            mock_search.assert_called_once()
            params = mock_search.call_args[0][0]
            self.assertEqual(params['damaged'], '0')
            self.assertEqual(params['pricefrom'], '15000')
            self.assertEqual(params['cy'], 'D')
    
    def test_extract_listing_data_basic(self):
        """Test extraction of basic listing data."""
        html = """
        <article>
            <h2>BMW 3er</h2>
            <a href="/detail/listing123"></a>
            <span class="Price_price__XGxpT">15.990 €</span>
            <ul>
                <li>50.000 km</li>
                <li>2020</li>
                <li>Diesel</li>
                <li>Automatik</li>
            </ul>
        </article>
        """
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        data = self.scraper._extract_listing_data(article)
        
        self.assertEqual(data['title'], 'BMW 3er')
        self.assertEqual(data['make'], 'BMW')
        self.assertEqual(data['model'], '3er')
        self.assertEqual(data['price'], 15990)
        self.assertEqual(data['mileage'], 50000)
        self.assertEqual(data['year'], 2020)
        self.assertEqual(data['fuel_type'], 'Diesel')
        self.assertEqual(data['transmission'], 'Automatic')
        self.assertIn('/detail/listing123', data['url'])
    
    def test_extract_listing_data_manual_transmission(self):
        """Test extraction with manual transmission."""
        html = """
        <article>
            <h2>VW Golf</h2>
            <ul>
                <li>Schaltgetriebe</li>
            </ul>
        </article>
        """
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        data = self.scraper._extract_listing_data(article)
        
        self.assertEqual(data['transmission'], 'Manual')
    
    def test_extract_listing_data_empty_element(self):
        """Test extraction with empty element."""
        html = "<article></article>"
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        data = self.scraper._extract_listing_data(article)
        
        # Should return default structure without errors
        self.assertEqual(data['title'], '')
        self.assertIsNone(data['price'])
        self.assertIsNone(data['mileage'])
    
    def test_parse_listings_no_elements(self):
        """Test parsing when no listing elements found."""
        html = "<html><body><div>No listings</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        listings = self.scraper._parse_listings(soup)
        
        self.assertEqual(len(listings), 0)
    
    @patch('scraper.autoscout_scraper.requests.Session.get')
    def test_search_listings_network_error(self, mock_get):
        """Test handling of network errors."""
        mock_get.side_effect = Exception("Network error")
        
        listings = self.scraper._search_listings({'test': 'param'})
        
        # Should return empty list on error
        self.assertEqual(listings, [])
    
    def test_url_construction(self):
        """Test that relative URLs are converted to absolute."""
        html = '<article><a href="/lst/detail123"></a></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        data = self.scraper._extract_listing_data(article)
        
        self.assertTrue(data['url'].startswith('https://www.autoscout24.de'))


class TestBaseScraper(unittest.TestCase):
    """Test cases for BaseScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a concrete implementation for testing
        class ConcreteScraper(BaseScraper):
            def search_broken_motors(self):
                return []
            def search_functional_cars(self, min_price=10000):
                return []
        
        self.scraper = ConcreteScraper()
    
    def test_init(self):
        """Test base scraper initialization."""
        self.assertIsNotNone(self.scraper.session)
        self.assertEqual(self.scraper.request_delay, 2)
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    def test_rate_limiting(self):
        """Test that rate limiting works."""
        import time
        
        with patch('scraper.base_scraper.requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.text = "test"
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Make first request
            start = time.time()
            self.scraper._make_request("http://test.com")
            
            # Make second request
            self.scraper._make_request("http://test.com")
            elapsed = time.time() - start
            
            # Should have waited at least request_delay seconds
            self.assertGreaterEqual(elapsed, self.scraper.request_delay - 0.1)


if __name__ == '__main__':
    unittest.main()
