# German Car Listings Analyzer

A comprehensive Python tool for scraping and analyzing German car listings from AutoScout24 and Mobile.de, comparing vehicles with broken motors against functional ones to identify market trends and price differences.

## Features

- 🚗 **Multi-Site Scraping**: Supports both AutoScout24.de and Mobile.de
- 🔍 **Intelligent Parsing**: Extracts detailed vehicle information including price, mileage, year, fuel type, and more
- 📊 **Data Analysis**: Comprehensive comparison between broken and functional motor vehicles
- 📈 **Visualizations**: Automatic generation of price comparison charts and statistics
- 🛡️ **Anti-Bot Measures**: Built-in user agent rotation, request delays, and stealth mode
- 📁 **Multiple Export Formats**: CSV and Excel outputs with detailed reports
- ⚙️ **Configurable**: Extensive configuration options for search parameters and scraping behavior

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/BViktar/german-car-listings-analyzer.git
cd german-car-listings-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. (Optional) Install in development mode:
```bash
pip install -e .
```

## Usage

### Basic Usage

Run the analyzer with default settings (scrapes both sites):

```bash
python -m src.broken_motor_parser
```

Or if installed as a package:

```bash
broken-motor-parser
```

### Advanced Usage

#### Scrape specific car make and model:

```bash
python -m src.broken_motor_parser --make BMW --model "3 Series"
```

#### Filter by year range:

```bash
python -m src.broken_motor_parser --year-min 2015 --year-max 2023
```

#### Limit maximum mileage:

```bash
python -m src.broken_motor_parser --mileage-max 150000
```

#### Scrape only one site:

```bash
# AutoScout24 only
python -m src.broken_motor_parser --site autoscout

# Mobile.de only
python -m src.broken_motor_parser --site mobile
```

#### Control scraping depth:

```bash
python -m src.broken_motor_parser --max-pages 5
```

#### Run in visible browser mode (for debugging):

```bash
python -m src.broken_motor_parser --headless false
```

#### Enable verbose logging:

```bash
python -m src.broken_motor_parser --verbose
```

### Complete Example

```bash
python -m src.broken_motor_parser \
    --make "Mercedes-Benz" \
    --model "C-Class" \
    --year-min 2018 \
    --year-max 2023 \
    --mileage-max 100000 \
    --max-pages 10 \
    --site both \
    --verbose
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--site` | Site to scrape: `autoscout`, `mobile`, or `both` | `both` |
| `--make` | Car manufacturer (e.g., BMW, Mercedes-Benz) | None |
| `--model` | Car model (e.g., 3 Series, C-Class) | None |
| `--year-min` | Minimum year | 2010 |
| `--year-max` | Maximum year | 2024 |
| `--mileage-max` | Maximum mileage in km | 200000 |
| `--max-pages` | Maximum pages to scrape per search | 10 |
| `--headless` | Run browser in headless mode | True |
| `--no-export` | Skip exporting results to files | False |
| `--verbose` | Enable verbose logging | False |

## Output Files

All output files are saved in the `output/` directory:

- **broken_motors.csv**: All broken motor listings
- **functional_motors.csv**: All functional motor listings
- **comparison_analysis.csv**: Comparison statistics
- **analysis_summary.xlsx**: Excel file with multiple sheets including summary
- **price_comparison.png**: Visual price comparison chart
- **scraper.log**: Detailed logging information

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── setup.py
└── src/
    ├── __init__.py
    ├── config.py                 # Configuration settings
    ├── broken_motor_parser.py    # Main script and CLI
    ├── scraper/
    │   ├── __init__.py
    │   ├── base_scraper.py       # Abstract base scraper
    │   ├── autoscout_scraper.py  # AutoScout24 implementation
    │   └── mobile_scraper.py     # Mobile.de implementation
    ├── analysis/
    │   ├── __init__.py
    │   └── data_processor.py     # Data analysis and processing
    └── utils/
        ├── __init__.py
        ├── browser.py            # Browser management
        └── export.py             # Data export utilities
```

## Configuration

### Environment Variables

Create a `.env` file in the project root for optional configuration:

```env
# Proxy settings (optional)
USE_PROXY=false
PROXY_URL=http://your-proxy-server:port
```

### Configuration File

Modify `src/config.py` to customize:

- Scraping delays and timeouts
- Browser settings
- Output file paths
- Search parameters
- Logging configuration

## Development

### Code Structure

The project follows object-oriented design principles:

- **BaseScraper**: Abstract base class defining the scraper interface
- **Site-specific scrapers**: Implement site-specific parsing logic
- **BrowserManager**: Handles browser lifecycle and anti-detection
- **DataProcessor**: Processes and analyzes scraped data
- **DataExporter**: Exports data to various formats

### Adding a New Scraper

To add support for a new car listing site:

1. Create a new scraper class in `src/scraper/` inheriting from `BaseScraper`
2. Implement all abstract methods:
   - `get_site_name()`
   - `build_search_url()`
   - `extract_listing_data()`
   - `get_listing_elements()`
   - `has_next_page()`
   - `go_to_next_page()`
3. Add the scraper to the main script in `src/broken_motor_parser.py`

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Add docstrings to all classes and methods
- Keep functions focused and modular

## Error Handling

The analyzer includes comprehensive error handling:

- **Retry Logic**: Automatic retries on network failures
- **Timeout Protection**: Configurable timeouts for page loads
- **Graceful Degradation**: Continues processing even if some listings fail
- **Detailed Logging**: All errors are logged with context

## Anti-Bot Measures

To avoid being blocked by websites:

- **Random Delays**: Variable delays between requests
- **User Agent Rotation**: Randomized user agents
- **Stealth Mode**: JavaScript modifications to hide automation
- **Rate Limiting**: Configurable request rates
- **Browser Fingerprinting**: Realistic browser configurations

## Limitations

- Scraping depends on website structure; updates to sites may require code changes
- Large-scale scraping may trigger anti-bot measures
- Some listings may have incomplete data
- Results accuracy depends on source data quality

## Troubleshooting

### Browser Installation Issues

If Playwright browsers aren't installing:

```bash
python -m playwright install chromium
```

### Import Errors

Ensure the project is installed or add to PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### No Results Found

- Check your search parameters aren't too restrictive
- Try running without `--headless` to see what's happening
- Enable `--verbose` for detailed logging
- Verify the websites are accessible from your location

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with the terms of service of the websites being scraped. The authors are not responsible for any misuse of this tool.

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Data analysis powered by [Pandas](https://pandas.pydata.org/)
- Visualizations created with [Matplotlib](https://matplotlib.org/)

## Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/BViktar/german-car-listings-analyzer/issues).
