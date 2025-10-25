# German Car Listings Analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Features

- **AutoScout24 Scraper**: Comprehensive web scraper for AutoScout24.de
  - Search for cars with broken motors ("Motorschaden")
  - Search for functional cars with price filtering
  - Robust error handling and rate limiting
  - Anti-blocking measures with realistic headers
  - Detailed logging for debugging
  - Type-safe implementation with type hints

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from scraper import AutoScout24Scraper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize scraper
scraper = AutoScout24Scraper()

# Search for cars with broken motors
broken_cars = scraper.search_broken_motors()
print(f"Found {len(broken_cars)} cars with broken motors")

# Search for functional cars (min price 15000 EUR)
functional_cars = scraper.search_functional_cars(min_price=15000)
print(f"Found {len(functional_cars)} functional cars")
```

### Running the Example Script

```bash
python example.py
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── scraper/
│       ├── __init__.py
│       ├── base_scraper.py       # Abstract base class
│       └── autoscout_scraper.py  # AutoScout24 implementation
├── tests/
│   ├── __init__.py
│   └── test_autoscout_scraper.py # Unit tests
├── example.py                     # Usage example
├── requirements.txt               # Dependencies
└── README.md
```

## Architecture

### BaseScraper (Abstract Base Class)

The `BaseScraper` class provides common functionality:
- HTTP session management with realistic headers
- Rate limiting (configurable delay between requests)
- Comprehensive error handling for network issues
- Abstract methods for search operations

### AutoScout24Scraper

The `AutoScout24Scraper` implements AutoScout24-specific functionality:

#### Methods

- `search_broken_motors()`: Search for damaged vehicles with "Motorschaden"
- `search_functional_cars(min_price)`: Search for functional cars above price threshold
- `_search_listings(params)`: Execute search with given parameters
- `_parse_listings(soup)`: Parse HTML search results
- `_extract_listing_data(element)`: Extract data from individual listing

#### Extracted Data

Each listing contains:
- `title`: Vehicle title
- `make`: Manufacturer
- `model`: Model name
- `year`: Year of manufacture
- `mileage`: Mileage in kilometers
- `price`: Price in EUR
- `fuel_type`: Fuel type (Benzin, Diesel, etc.)
- `transmission`: Transmission type (Automatic/Manual)
- `url`: Listing URL
- `location`: Vehicle location
- `seller_type`: Type of seller

## Features in Detail

### Error Handling

- Network timeout handling
- Connection error recovery
- HTTP error status handling
- Graceful parsing error handling
- Detailed error logging

### Rate Limiting

- Configurable delay between requests (default: 3 seconds for AutoScout24)
- Automatic sleep between consecutive requests
- Prevents server blocking

### Anti-Blocking Measures

- Realistic browser User-Agent headers
- Standard HTTP headers (Accept, Accept-Language, etc.)
- Request throttling
- Session persistence

### Logging

- Comprehensive logging at different levels (INFO, DEBUG, ERROR)
- Request tracking
- Error stack traces for debugging
- Configurable output (console and file)

## Testing

Run the test suite:

```bash
python -m unittest tests.test_autoscout_scraper -v
```

Tests cover:
- Scraper initialization
- Parameter generation for different search types
- HTML parsing with various structures
- Data extraction from listing elements
- Error handling for network issues
- Rate limiting functionality
- URL construction

## Dependencies

- `beautifulsoup4`: HTML parsing
- `requests`: HTTP client
- `lxml`: Fast HTML parser for BeautifulSoup

## Notes

- AutoScout24's HTML structure may change over time; the scraper uses multiple selectors for robustness
- Rate limiting is crucial to avoid being blocked
- Always respect the website's robots.txt and terms of service
- This is for educational/research purposes only

## License

See LICENSE file for details.
