# German Car Listings Analyzer

Python project for analyzing German car listings, comparing vehicles with broken motors against functional ones.

## Overview

This project scrapes and analyzes car listings from German automotive marketplaces, with a focus on comparing vehicles with broken motors to their functional counterparts. The analysis helps identify pricing patterns, market trends, and potential value opportunities.

## Features

- **Web Scraping**: Automated scraping of car listings from German automotive websites
- **Broken Motor Parsing**: Specialized parser for identifying and extracting listings with broken motors
- **Data Analysis**: Statistical analysis and comparison of broken vs. functional vehicles
- **Configuration Management**: Flexible configuration system for customizing scraping and analysis parameters

## Project Structure

```
german-car-listings-analyzer/
├── src/
│   ├── broken_motor_parser.py  # Parser for broken motor listings
│   ├── config.py                # Configuration management
│   ├── scraper/                 # Web scraping modules
│   │   ├── __init__.py
│   │   └── base_scraper.py
│   ├── analysis/                # Data analysis modules
│   │   ├── __init__.py
│   │   └── analyzer.py
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt             # Project dependencies
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BViktar/german-car-listings-analyzer.git
cd german-car-listings-analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

(To be implemented)

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Development

This project is in active development. Contributions are welcome!

## License

See LICENSE file for details.
