# Car Listing Scrapers

This module provides scrapers for German car listing websites to analyze and compare vehicles with broken motors against functional ones.

## Features

- **Base Scraper Framework**: Abstract base class for implementing car listing scrapers
- **AutoScout24 Scraper**: Implementation for AutoScout24.de
- **Mobile.de Scraper**: Implementation for Mobile.de
- **Anti-blocking Measures**: 
  - User agent rotation (7 different user agents)
  - Random delays between requests (1-3 seconds)
- **Error Handling**: Comprehensive error handling and logging
- **Structured Data**: Returns parsed listings as dictionaries

## Installation

Install the package in development mode:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## Usage

### Basic Usage

```python
from src.scraper import AutoScout24Scraper, MobileScraper
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# AutoScout24 Example
autoscout = AutoScout24Scraper()

# Search for broken motor cars
broken_cars = autoscout.search_broken_motors()
print(f"Found {len(broken_cars)} broken motor listings")

# Search for functional cars above €10,000
functional_cars = autoscout.search_functional_cars(min_price=10000)
print(f"Found {len(functional_cars)} functional car listings")

# Mobile.de Example
mobile = MobileScraper()

# Search for broken motor cars
broken_cars = mobile.search_broken_motors()
print(f"Found {len(broken_cars)} broken motor listings")

# Search for functional cars above €15,000
functional_cars = mobile.search_functional_cars(min_price=15000)
print(f"Found {len(functional_cars)} functional car listings")
```

### Running Examples

```bash
# Run basic tests
python test_scrapers.py

# Run example usage (makes actual HTTP requests)
python example_usage.py
```

## Architecture

### BaseScraper

Abstract base class that provides:
- `search_broken_motors()`: Abstract method to search for cars with broken motors
- `search_functional_cars(min_price)`: Abstract method to search for functional cars
- `_load_user_agents()`: Load user agents for rotation
- `_implement_delay()`: Random delay mechanism (1-3 seconds)
- `_get_random_user_agent()`: Get a random user agent
- `_handle_request_error()`: Error handling helper

### AutoScout24Scraper

Implements scraping for AutoScout24.de:
- Inherits from `BaseScraper`
- Uses BeautifulSoup for HTML parsing
- Implements site-specific search parameters and parsing logic
- Returns structured data with fields: source, title, price, mileage, year, url, etc.

### MobileScraper

Implements scraping for Mobile.de:
- Inherits from `BaseScraper`
- Uses BeautifulSoup for HTML parsing
- Implements site-specific search parameters and parsing logic
- Returns structured data with fields: source, title, price, mileage, year, url, location, etc.

## Data Structure

Each scraper returns a list of dictionaries with the following structure:

```python
{
    'source': 'AutoScout24' or 'Mobile.de',
    'broken_motor': True or False,
    'title': 'Car make and model',
    'price': 12345,  # Numeric price
    'price_text': '€12,345',  # Original price text
    'mileage': '50,000 km',
    'year': '2018',
    'url': 'https://...',
    'location': 'Berlin'  # Mobile.de only
}
```

## Anti-blocking Features

1. **User Agent Rotation**: Randomly selects from 7 different modern browser user agents
2. **Request Delays**: Implements random delays (1-3 seconds) between requests
3. **Error Handling**: Gracefully handles request errors and continues operation
4. **Session Management**: Uses persistent HTTP sessions for better performance

## Logging

The scrapers use Python's built-in logging module. Configure logging in your application:

```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or configure with file output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log')
    ]
)
```

## Error Handling

All scrapers include:
- Try-except blocks around HTTP requests
- Timeout handling (30 seconds default)
- Graceful degradation (returns empty list on errors)
- Detailed error logging

## Extending the Framework

To add a new car listing site:

1. Create a new scraper class that inherits from `BaseScraper`
2. Implement the abstract methods:
   - `search_broken_motors()`
   - `search_functional_cars(min_price)`
3. Add site-specific parsing logic
4. Register in `src/scraper/__init__.py`

Example:

```python
import requests
from src.scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    BASE_URL = "https://example.com"
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
    
    def search_broken_motors(self):
        # Implementation
        pass
    
    def search_functional_cars(self, min_price=10000):
        # Implementation
        pass
```

## Important Notes

- **Website Structure**: The parsing logic is based on the current website structure. If the websites change their HTML structure, the parsers may need updates.
- **Rate Limiting**: Respect the websites' terms of service and implement appropriate delays.
- **Legal Compliance**: Ensure your use case complies with the websites' terms of service and local laws.
- **Data Accuracy**: The scrapers parse publicly available data, but accuracy depends on the source websites.

## License

See the LICENSE file in the repository root.
