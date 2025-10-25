# German Car Listings Analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Features

The project provides a comprehensive visualization and reporting component for car comparison analysis, including:

- **Price Comparison Visualizations**: Box plots and bar charts comparing prices between broken and functional vehicles
- **Age Distribution Analysis**: Histograms showing the age distribution of vehicles
- **Mileage Comparison**: Box plots comparing mileage between vehicle categories
- **Excel Reports**: Detailed statistical reports exported to Excel format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BViktar/german-car-listings-analyzer.git
cd german-car-listings-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.utils.visualization import CarDataVisualizer

# Create visualizer instance
visualizer = CarDataVisualizer(output_dir='output')

# Prepare your analysis data
analysis_data = {
    'price_comparison': {
        'broken': [5000, 6000, 5500],
        'functional': [15000, 16000, 15500],
        'broken_avg': 5500,
        'functional_avg': 15500,
        # ... more statistics
    },
    'age_distribution': {
        'broken': [5, 6, 7],
        'functional': [2, 3, 4],
        # ... more statistics
    },
    # ... more analysis data
}

# Generate visualizations
visualizer.create_price_comparison(analysis_data)
visualizer.create_age_distribution(analysis_data)
visualizer.create_mileage_comparison(analysis_data)

# Export to Excel
visualizer.export_excel_report(analysis_data)
```

### Running the Example

```bash
python example_usage.py
```

This will generate sample visualizations and reports in the `output/` directory.

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   └── utils/
│       ├── __init__.py
│       └── visualization.py    # Main visualization module
├── tests/
│   ├── __init__.py
│   └── test_visualization.py   # Comprehensive tests
├── example_usage.py             # Example usage script
├── requirements.txt             # Project dependencies
├── pytest.ini                   # Pytest configuration
├── .flake8                      # Linting configuration
├── .gitignore
└── README.md
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

## Linting

Check code quality:

```bash
flake8 src/ tests/
```

## Dependencies

- **pandas** (>=2.0.0): Data manipulation and Excel export
- **matplotlib** (>=3.7.0): Plotting and visualization
- **seaborn** (>=0.12.0): Statistical visualization
- **openpyxl** (>=3.1.0): Excel file support
- **pytest** (>=7.4.0): Testing framework

## Output

The visualizer generates the following files in the output directory:

1. **price_distribution.png**: Box plot comparing price distributions
2. **model_price_comparison.png**: Bar chart comparing average prices by model
3. **age_distribution.png**: Histogram showing age distributions
4. **mileage_comparison.png**: Box plot comparing mileage distributions
5. **car_analysis.xlsx**: Comprehensive Excel report with multiple sheets:
   - Price Analysis
   - Model Statistics
   - Mileage Analysis
   - Age Analysis
   - Summary

## License

This project is licensed under the MIT License - see the LICENSE file for details.

