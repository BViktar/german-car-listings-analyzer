"""Example script demonstrating the Mobile.de scraper usage."""

import logging
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper.mobile_scraper import MobileDeScraper


def main():
    """Main example function."""
    # Configure logging to see what's happening
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("German Car Listings Analyzer - Mobile.de Scraper Example")
    print("=" * 60)
    print()
    
    # Initialize the scraper
    scraper = MobileDeScraper()
    print("✓ Scraper initialized")
    print()
    
    # Example 1: Search for cars with broken motors
    print("Example 1: Searching for cars with broken motors...")
    print("-" * 60)
    try:
        broken_cars = scraper.search_broken_motors()
        print(f"Found {len(broken_cars)} cars with broken motors")
        
        if broken_cars:
            print("\nFirst 3 results:")
            for i, car in enumerate(broken_cars[:3], 1):
                print(f"\n{i}. {car['title']}")
                print(f"   Price: €{car['price'] if car['price'] else 'N/A'}")
                print(f"   Year: {car['year'] if car['year'] else 'N/A'}")
                print(f"   Mileage: {car['mileage'] if car['mileage'] else 'N/A'} km")
                print(f"   URL: {car['url']}")
    except Exception as e:
        print(f"Error searching for broken motors: {e}")
    
    print()
    print("=" * 60)
    print()
    
    # Example 2: Search for functional cars above €10,000
    print("Example 2: Searching for functional cars above €10,000...")
    print("-" * 60)
    try:
        functional_cars = scraper.search_functional_cars(min_price=10000)
        print(f"Found {len(functional_cars)} functional cars")
        
        if functional_cars:
            print("\nFirst 3 results:")
            for i, car in enumerate(functional_cars[:3], 1):
                print(f"\n{i}. {car['title']}")
                print(f"   Price: €{car['price'] if car['price'] else 'N/A'}")
                print(f"   Year: {car['year'] if car['year'] else 'N/A'}")
                print(f"   Mileage: {car['mileage'] if car['mileage'] else 'N/A'} km")
                print(f"   Fuel: {car['fuel_type']}")
                print(f"   Transmission: {car['transmission']}")
                print(f"   URL: {car['url']}")
    except Exception as e:
        print(f"Error searching for functional cars: {e}")
    
    print()
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
