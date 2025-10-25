import logging
from pathlib import Path
from typing import Dict, List
from scraper.autoscout_scraper import AutoScout24Scraper
from scraper.mobile_scraper import MobileDeScraper
from utils.csv_report import CarReportGenerator

def main():
    """Main function to scrape car listings and generate reports."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize scrapers
        autoscout = AutoScout24Scraper()
        mobile = MobileDeScraper()
        
        # Initialize report generator
        report_generator = CarReportGenerator(output_dir='reports')
        
        logger.info("Starting car listings search...")
        
        # Fetch broken motor listings
        broken_cars_as24 = autoscout.search_broken_motors()
        broken_cars_mobile = mobile.search_broken_motors()
        broken_cars = broken_cars_as24 + broken_cars_mobile
        
        logger.info(f"Found {len(broken_cars)} cars with broken motors")
        
        # Fetch functional car listings
        functional_cars_as24 = autoscout.search_functional_cars()
        functional_cars_mobile = mobile.search_functional_cars()
        functional_cars = functional_cars_as24 + functional_cars_mobile
        
        logger.info(f"Found {len(functional_cars)} functional cars for comparison")
        
        # Generate reports
        logger.info("Generating CSV reports...")
        report_generator.generate_reports(broken_cars, functional_cars)
        
        logger.info("Reports generated successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == '__main__':
    main()
