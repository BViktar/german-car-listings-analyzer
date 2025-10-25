"""Example usage of the AutoScout24 scraper."""
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import AutoScout24Scraper


def setup_logging():
    """Configure logging for the example."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('scraper.log')
        ]
    )


def main():
    """Main example function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting AutoScout24 scraper example")
    
    # Initialize scraper
    scraper = AutoScout24Scraper()
    
    # Example 1: Search for cars with broken motors
    logger.info("=" * 50)
    logger.info("Searching for cars with broken motors...")
    logger.info("=" * 50)
    broken_cars = scraper.search_broken_motors()
    logger.info(f"Found {len(broken_cars)} cars with broken motors")
    
    if broken_cars:
        logger.info("\nFirst 3 results:")
        for i, car in enumerate(broken_cars[:3], 1):
            logger.info(f"\n{i}. {car['title']}")
            logger.info(f"   Price: {car['price']} EUR" if car['price'] else "   Price: N/A")
            logger.info(f"   Year: {car['year']}" if car['year'] else "   Year: N/A")
            logger.info(f"   Mileage: {car['mileage']} km" if car['mileage'] else "   Mileage: N/A")
            logger.info(f"   URL: {car['url']}" if car['url'] else "   URL: N/A")
    
    # Example 2: Search for functional cars
    logger.info("\n" + "=" * 50)
    logger.info("Searching for functional cars (min price: 15000 EUR)...")
    logger.info("=" * 50)
    functional_cars = scraper.search_functional_cars(min_price=15000)
    logger.info(f"Found {len(functional_cars)} functional cars")
    
    if functional_cars:
        logger.info("\nFirst 3 results:")
        for i, car in enumerate(functional_cars[:3], 1):
            logger.info(f"\n{i}. {car['title']}")
            logger.info(f"   Make: {car['make']}, Model: {car['model']}")
            logger.info(f"   Price: {car['price']} EUR" if car['price'] else "   Price: N/A")
            logger.info(f"   Year: {car['year']}" if car['year'] else "   Year: N/A")
            logger.info(f"   Fuel: {car['fuel_type']}" if car['fuel_type'] else "   Fuel: N/A")
            logger.info(f"   Transmission: {car['transmission']}" if car['transmission'] else "   Transmission: N/A")
    
    logger.info("\n" + "=" * 50)
    logger.info("Example completed successfully!")
    logger.info("=" * 50)


if __name__ == '__main__':
    main()
