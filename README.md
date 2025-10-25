# German Car Listings Analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Features

- **Mobile.de Scraper**: Comprehensive scraper for Mobile.de car listings
- **Broken Motor Search**: Search for cars with "Motorschaden" (broken motors)
- **Functional Car Search**: Search for functional vehicles above a minimum price
- **Rate Limiting**: Built-in rate limiting to avoid blocking
- **Error Handling**: Robust error handling for network and parsing issues
- **Logging**: Detailed logging for debugging and monitoring

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.scraper.mobile_scraper import MobileDeScraper

# Initialize the scraper
scraper = MobileDeScraper()

# Search for cars with broken motors
broken_cars = scraper.search_broken_motors()
print(f"Found {len(broken_cars)} cars with broken motors")

# Search for functional cars above €10,000
functional_cars = scraper.search_functional_cars(min_price=10000)
print(f"Found {len(functional_cars)} functional cars")

# Access listing data
for car in broken_cars[:5]:  # First 5 results
    print(f"{car['title']}: €{car['price']}")
```

### Advanced Usage

```python
import logging
from src.scraper.mobile_scraper import MobileDeScraper

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize scraper
scraper = MobileDeScraper()

# Search for premium functional cars
premium_cars = scraper.search_functional_cars(min_price=25000)

# Filter and analyze results
for car in premium_cars:
    if car['year'] and car['year'] >= 2020:
        print(f"Recent {car['make']} {car['model']}: €{car['price']}")
```

## Data Structure

Each car listing contains the following fields:

```python
{
    'title': str,           # Full title of the listing
    'make': str,            # Car manufacturer (e.g., "BMW")
    'model': str,           # Car model (e.g., "320d")
    'year': int,            # Year of first registration
    'mileage': int,         # Mileage in kilometers
    'price': int,           # Price in euros
    'fuel_type': str,       # Fuel type (e.g., "Diesel", "Benzin")
    'transmission': str,    # Transmission type (e.g., "Automatic", "Manual")
    'url': str             # Direct URL to the listing
}
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests/
```

## Features

### Rate Limiting

The scraper includes built-in rate limiting (default: 1 second between requests) to avoid being blocked:

```python
scraper = MobileDeScraper()
scraper.rate_limit = 2.0  # 2 seconds between requests
```

### Error Handling

The scraper handles various error scenarios:
- Network timeouts and connection errors
- HTML parsing errors
- Missing data fields
- Invalid data formats

All errors are logged with appropriate detail levels.

### Anti-Blocking Measures

- Realistic User-Agent headers
- Automatic retry with exponential backoff
- Rate limiting between requests
- Connection pooling and keep-alive

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   └── scraper/
│       ├── __init__.py
│       ├── base_scraper.py      # Abstract base class
│       └── mobile_scraper.py    # Mobile.de implementation
├── tests/
│   ├── __init__.py
│   └── test_mobile_scraper.py   # Unit tests
├── requirements.txt
├── setup.py
└── README.md
```

## Requirements

- Python 3.8+
- beautifulsoup4 >= 4.12.0
- requests >= 2.31.0
- urllib3 >= 2.0.0
- lxml >= 4.9.0

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and research purposes only. Please respect Mobile.de's Terms of Service and robots.txt when using this scraper. Always use rate limiting and avoid excessive requests.
