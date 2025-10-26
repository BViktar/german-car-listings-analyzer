"""
Main script for generating car comparison reports.

This script coordinates the scraping of car listings from AutoScout24 and Mobile.de,
and generates comprehensive CSV reports comparing broken motor cars with functional cars.
"""
import logging
from pathlib import Path
from datetime import datetime
from scraper.autoscout_scraper import AutoScout24Scraper
from scraper.mobile_scraper import MobileDeScraper
from utils.csv_report import CarReportGenerator


def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main function to generate car comparison reports."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize scrapers
        autoscout = AutoScout24Scraper()
        mobile = MobileDeScraper()
        
        # Initialize report generator
        report_dir = Path('reports') / datetime.now().strftime('%Y%m%d_%H%M%S')
        report_generator = CarReportGenerator(str(report_dir))
        
        logger.info("Fetching broken cars listings...")
        # Get broken cars listings
        broken_cars_as24 = autoscout.search_broken_motors()
        broken_cars_mobile = mobile.search_broken_motors()
        broken_cars = broken_cars_as24 + broken_cars_mobile
        
        logger.info("Fetching functional cars listings...")
        # Get functional cars listings
        functional_cars_as24 = autoscout.search_functional_cars(min_price=10000)
        functional_cars_mobile = mobile.search_functional_cars(min_price=10000)
        functional_cars = functional_cars_as24 + functional_cars_mobile
        
        logger.info("Generating reports...")
        # Generate reports
        report_generator.generate_reports(broken_cars, functional_cars)
        
        logger.info(f"Reports generated successfully in: {report_dir}")
        
    except Exception as e:
        logger.error(f"Error generating reports: {str(e)}")
        raise


if __name__ == "__main__":
    main()
