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
