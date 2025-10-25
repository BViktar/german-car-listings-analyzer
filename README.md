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
