"""Example usage of the car listing scrapers."""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import AutoScout24Scraper, MobileScraper


def setup_logging():
    """Setup detailed logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scraper.log')
        ]
    )


def example_autoscout24():
    """Example usage of AutoScout24 scraper."""
    print("\n" + "=" * 70)
    print("AutoScout24 Scraper Example")
    print("=" * 70)
    
    scraper = AutoScout24Scraper()
    
    # Example 1: Search for broken motor cars
    print("\n1. Searching for cars with broken motors...")
    broken_cars = scraper.search_broken_motors()
    print(f"   Found {len(broken_cars)} broken motor listings")
    if broken_cars:
        print(f"   Sample: {broken_cars[0]}")
    
    # Example 2: Search for functional cars above 15000 EUR
    print("\n2. Searching for functional cars above €15,000...")
    functional_cars = scraper.search_functional_cars(min_price=15000)
    print(f"   Found {len(functional_cars)} functional car listings")
    if functional_cars:
        print(f"   Sample: {functional_cars[0]}")


def example_mobile():
    """Example usage of Mobile.de scraper."""
    print("\n" + "=" * 70)
    print("Mobile.de Scraper Example")
    print("=" * 70)
    
    scraper = MobileScraper()
    
    # Example 1: Search for broken motor cars
    print("\n1. Searching for cars with broken motors...")
    broken_cars = scraper.search_broken_motors()
    print(f"   Found {len(broken_cars)} broken motor listings")
    if broken_cars:
        print(f"   Sample: {broken_cars[0]}")
    
    # Example 2: Search for functional cars above 20000 EUR
    print("\n2. Searching for functional cars above €20,000...")
    functional_cars = scraper.search_functional_cars(min_price=20000)
    print(f"   Found {len(functional_cars)} functional car listings")
    if functional_cars:
        print(f"   Sample: {functional_cars[0]}")


def main():
    """Run example usage of both scrapers."""
    setup_logging()
    
    print("=" * 70)
    print("German Car Listings Analyzer - Example Usage")
    print("=" * 70)
    print("\nNote: This example will make actual HTTP requests to websites.")
    print("The results may vary based on current listings and website structure.")
    print("Logs are saved to 'scraper.log'")
    
    try:
        # Run AutoScout24 examples
        example_autoscout24()
        
        # Run Mobile.de examples
        example_mobile()
        
        print("\n" + "=" * 70)
        print("Examples completed! Check 'scraper.log' for detailed logs.")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError during execution: {e}")
        logging.exception("Unexpected error in main")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
