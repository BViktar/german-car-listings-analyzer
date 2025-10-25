# german-car-listings-analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Features

The `CarComparisonAnalyzer` provides comprehensive analysis capabilities:

- **Price Analysis**: Statistical comparison of prices between broken and functional cars
- **Age Distribution**: Analysis of vehicle age patterns
- **Mileage Analysis**: Comparison of mileage statistics
- **Model Statistics**: Per make/model breakdown and comparisons
- **Summary Reports**: High-level overview with key insights

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.analysis.comparison_analyzer import CarComparisonAnalyzer

# Sample data
broken_cars = [
    {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 5000, 'mileage': 120000},
    # ... more cars
]

functional_cars = [
    {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 15000, 'mileage': 80000},
    # ... more cars
]

# Analyze
analyzer = CarComparisonAnalyzer()
result = analyzer.analyze_listings(broken_cars, functional_cars)

# Access results
print(f"Average price difference: €{result.summary['average_price_difference']:.2f}")
print(f"Broken cars mean price: €{result.price_comparison['broken']['mean']:.2f}")
```

## Running Tests

```bash
python -m unittest tests.test_comparison_analyzer -v
```

## Running the Example

```bash
python example.py
```

## Requirements

- pandas >= 1.5.0
- numpy >= 1.23.0

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   └── analysis/
│       └── comparison_analyzer.py
├── tests/
│   └── test_comparison_analyzer.py
├── example.py
├── requirements.txt
└── README.md
```
