"""Main script for German Car Listings Analyzer."""

import argparse
import logging
import logging.config
import sys
from typing import Optional

from src.config import LOGGING_CONFIG, SCRAPING_CONFIG, SEARCH_PARAMS
from src.scraper.autoscout_scraper import AutoScout24Scraper
from src.scraper.mobile_scraper import MobileDeScraper
from src.analysis.data_processor import DataProcessor
from src.utils.browser import BrowserManager
from src.utils.export import DataExporter

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.config.dictConfig(LOGGING_CONFIG)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="German Car Listings Analyzer - Compare broken vs functional car prices"
    )
    
    parser.add_argument(
        '--site',
        type=str,
        choices=['autoscout', 'mobile', 'both'],
        default='both',
        help='Which site(s) to scrape (default: both)'
    )
    
    parser.add_argument(
        '--make',
        type=str,
        help='Car manufacturer (e.g., BMW, Mercedes-Benz)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Car model (e.g., 3 Series, C-Class)'
    )
    
    parser.add_argument(
        '--year-min',
        type=int,
        default=SEARCH_PARAMS['default_filters']['year_min'],
        help='Minimum year'
    )
    
    parser.add_argument(
        '--year-max',
        type=int,
        default=SEARCH_PARAMS['default_filters']['year_max'],
        help='Maximum year'
    )
    
    parser.add_argument(
        '--mileage-max',
        type=int,
        default=SEARCH_PARAMS['default_filters']['mileage_max'],
        help='Maximum mileage in km'
    )
    
    parser.add_argument(
        '--max-pages',
        type=int,
        default=SCRAPING_CONFIG['max_pages'],
        help='Maximum number of pages to scrape per search'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        default=SCRAPING_CONFIG['headless'],
        help='Run browser in headless mode'
    )
    
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip exporting results to files'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def scrape_site(
    scraper_class,
    browser_manager: BrowserManager,
    search_params: dict,
    max_pages: int,
    damaged: bool,
) -> list:
    """
    Scrape a single site.
    
    Args:
        scraper_class: Scraper class to instantiate
        browser_manager: BrowserManager instance
        search_params: Search parameters
        max_pages: Maximum pages to scrape
        damaged: Whether to search for damaged cars
        
    Returns:
        List of scraped listings
    """
    scraper = scraper_class(browser_manager)
    
    # Add damaged filter
    scrape_params = search_params.copy()
    scrape_params['damaged'] = damaged
    
    try:
        results = scraper.scrape(search_params=scrape_params, max_pages=max_pages)
        return results
    except Exception as e:
        logger.error(f"Error scraping {scraper.get_site_name()}: {e}", exc_info=True)
        return []


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Setup logging
    setup_logging()
    
    # Parse arguments
    args = parse_arguments()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 80)
    logger.info("German Car Listings Analyzer")
    logger.info("=" * 80)
    
    # Prepare search parameters
    search_params = {
        'make': args.make,
        'model': args.model,
        'year_min': args.year_min,
        'year_max': args.year_max,
        'mileage_max': args.mileage_max,
    }
    
    # Remove None values
    search_params = {k: v for k, v in search_params.items() if v is not None}
    
    logger.info(f"Search parameters: {search_params}")
    logger.info(f"Max pages per search: {args.max_pages}")
    
    # Initialize browser manager
    browser_manager = BrowserManager(
        headless=args.headless,
        browser_type=SCRAPING_CONFIG['browser_type']
    )
    
    broken_motors_data = []
    functional_motors_data = []
    
    try:
        browser_manager.start()
        
        # Determine which sites to scrape
        sites = []
        if args.site in ['autoscout', 'both']:
            sites.append(AutoScout24Scraper)
        if args.site in ['mobile', 'both']:
            sites.append(MobileDeScraper)
        
        # Scrape broken motors
        logger.info("\n" + "=" * 80)
        logger.info("SCRAPING BROKEN MOTOR LISTINGS")
        logger.info("=" * 80)
        
        for scraper_class in sites:
            results = scrape_site(
                scraper_class,
                browser_manager,
                search_params,
                args.max_pages,
                damaged=True
            )
            broken_motors_data.extend(results)
            logger.info(f"Total broken motors collected: {len(broken_motors_data)}")
        
        # Scrape functional motors
        logger.info("\n" + "=" * 80)
        logger.info("SCRAPING FUNCTIONAL MOTOR LISTINGS")
        logger.info("=" * 80)
        
        for scraper_class in sites:
            results = scrape_site(
                scraper_class,
                browser_manager,
                search_params,
                args.max_pages,
                damaged=False
            )
            functional_motors_data.extend(results)
            logger.info(f"Total functional motors collected: {len(functional_motors_data)}")
        
    except KeyboardInterrupt:
        logger.warning("\nScraping interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error during scraping: {e}", exc_info=True)
        return 1
    finally:
        browser_manager.stop()
    
    # Check if we have data
    if not broken_motors_data and not functional_motors_data:
        logger.error("No data was collected. Exiting.")
        return 1
    
    # Process and analyze data
    logger.info("\n" + "=" * 80)
    logger.info("DATA PROCESSING AND ANALYSIS")
    logger.info("=" * 80)
    
    try:
        processor = DataProcessor()
        processor.load_data(broken_motors_data, functional_motors_data)
        processor.clean_data()
        
        # Perform analysis
        comparison_df = processor.analyze()
        
        # Get DataFrames
        broken_df, functional_df, comparison_df = processor.get_dataframes()
        
        # Print summary
        logger.info("\n" + "-" * 80)
        logger.info("ANALYSIS SUMMARY")
        logger.info("-" * 80)
        print("\n" + str(comparison_df.to_string(index=False)))
        
        # Get detailed statistics
        stats = processor.get_statistics()
        logger.info("\n" + "-" * 80)
        logger.info("DETAILED STATISTICS")
        logger.info("-" * 80)
        logger.info(f"\nBroken Motors: {stats.get('broken_motors', {}).get('total_count', 0)} listings")
        if 'broken_motors' in stats and 'price' in stats['broken_motors']:
            price_stats = stats['broken_motors']['price']
            logger.info(f"  Price - Mean: €{price_stats['mean']:,.2f}, "
                       f"Median: €{price_stats['median']:,.2f}, "
                       f"Range: €{price_stats['min']:,.2f} - €{price_stats['max']:,.2f}")
        
        logger.info(f"\nFunctional Motors: {stats.get('functional_motors', {}).get('total_count', 0)} listings")
        if 'functional_motors' in stats and 'price' in stats['functional_motors']:
            price_stats = stats['functional_motors']['price']
            logger.info(f"  Price - Mean: €{price_stats['mean']:,.2f}, "
                       f"Median: €{price_stats['median']:,.2f}, "
                       f"Range: €{price_stats['min']:,.2f} - €{price_stats['max']:,.2f}")
        
        # Export results
        if not args.no_export:
            logger.info("\n" + "=" * 80)
            logger.info("EXPORTING RESULTS")
            logger.info("=" * 80)
            
            DataExporter.generate_full_report(
                broken_df,
                functional_df,
                comparison_df
            )
            
            logger.info("\nExport completed successfully!")
        
        logger.info("\n" + "=" * 80)
        logger.info("ANALYSIS COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
