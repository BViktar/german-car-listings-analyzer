# German Car Listings Analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Overview

This project scrapes car listings from popular German automotive websites (AutoScout24 and Mobile.de) and generates comprehensive CSV reports comparing broken motor vehicles with functional cars. The analysis helps identify potential savings and market trends.

## Features

- Scrapes broken motor car listings from AutoScout24 and Mobile.de
- Fetches functional car listings with customizable price filters
- Generates detailed CSV reports:
  - `broken_cars.csv` - All broken motor listings
  - `functional_cars.csv` - All functional car listings  
  - `comparison_summary.csv` - Statistical comparison and analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BViktar/german-car-listings-analyzer.git
cd german-car-listings-analyzer
```

2. Install dependencies (optional - currently uses standard library only):
# german-car-listings-analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Features

- **CSV Report Generation**: Generate comprehensive reports comparing broken cars with functional similar models
- **Price Analysis**: Calculate average prices for similar functional cars
- **Linked Reports**: Main report links to detailed similar car listings
- **UTF-8 Support**: Full support for German characters (ä, ö, ü, ß)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to generate reports:

```bash
PYTHONPATH=/path/to/german-car-listings-analyzer:$PYTHONPATH python src/generate_reports.py
```

Or from the project root:

```bash
PYTHONPATH=.:$PYTHONPATH python src/generate_reports.py
```

Reports will be generated in the `reports/YYYYMMDD_HHMMSS/` directory.

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   └── generate_reports.py    # Main script
├── scraper/
│   ├── autoscout_scraper.py   # AutoScout24 scraper
│   └── mobile_scraper.py      # Mobile.de scraper
├── utils/
│   └── csv_report.py          # Report generator
├── reports/                    # Generated reports (gitignored)
└── requirements.txt            # Python dependencies
```

## Documentation

### Modules

#### `src/generate_reports.py`
Main script that coordinates scraping and report generation with proper logging and error handling.

#### `scraper/autoscout_scraper.py`
AutoScout24Scraper class for fetching car listings from AutoScout24.de.

#### `scraper/mobile_scraper.py`
MobileDeScraper class for fetching car listings from Mobile.de.

#### `utils/csv_report.py`
CarReportGenerator class for generating CSV reports with statistical analysis.

## Future Enhancements

- Implement actual web scraping (currently uses mock data)
- Add more search filters (make, model, year range, location)
- Support additional car listing websites
- Add data visualization and charts
- Implement caching to avoid repeated scraping

## License

See LICENSE file for details.
### Basic Example

```python
from src.utils.csv_report import CarReportGenerator

# Sample data
broken_cars = [
    {
        'make': 'BMW',
        'model': '320i',
        'year': 2015,
        'price': 5000,
        'url': 'https://www.mobile.de/broken-car'
    }
]

functional_cars = [
    {
        'make': 'BMW',
        'model': '320i',
        'year': 2015,
        'price': 12000,
        'mileage': 80000,
        'url': 'https://www.mobile.de/functional-car'
    }
]

# Generate reports
generator = CarReportGenerator(output_dir='reports')
generator.generate_reports(broken_cars, functional_cars)
```

### Running the Example

```bash
python example.py
```

This will generate:
- `reports/broken_cars_report.csv` - Main report with broken cars and average prices
- `reports/similar_cars_<make>_<model>.csv` - Individual reports for each make/model combination

## Report Structure

### Main Report (broken_cars_report.csv)

| Column | Description |
|--------|-------------|
| car_description | Full description (year, make, model) |
| advertisement_link | URL to the listing |
| price | Price of the broken car |
| average_similar_price | Average price of similar functional cars |
| similar_cars_file | Link to similar cars CSV file |

### Similar Cars Reports (similar_cars_*.csv)

| Column | Description |
|--------|-------------|
| make | Car manufacturer |
| model | Car model |
| year | Year of manufacture |
| price | Price of the car |
| mileage | Mileage in km |
| url | URL to the listing |

## Testing

```bash
pytest tests/test_csv_report.py -v
```

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   └── utils/
│       └── csv_report.py    # Main CSV report generator
├── tests/
│   └── test_csv_report.py   # Comprehensive test suite
├── example.py               # Usage example
├── requirements.txt         # Project dependencies
└── README.md               # This file
```
