#!/usr/bin/env python3
"""
Simple test script to verify the main script functionality.
"""
import sys
import os
import logging
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.autoscout_scraper import AutoScout24Scraper
from scraper.mobile_scraper import MobileDeScraper
from utils.csv_report import CarReportGenerator


def test_scrapers():
    """Test scraper initialization and basic functionality."""
    print("Testing scrapers...")
    
    # Test AutoScout24Scraper
    autoscout = AutoScout24Scraper()
    broken_cars_as = autoscout.search_broken_motors()
    functional_cars_as = autoscout.search_functional_cars(min_price=10000)
    
    assert len(broken_cars_as) > 0, "AutoScout24 should return broken cars"
    assert len(functional_cars_as) > 0, "AutoScout24 should return functional cars"
    print(f"✓ AutoScout24Scraper: {len(broken_cars_as)} broken, {len(functional_cars_as)} functional")
    
    # Test MobileDeScraper
    mobile = MobileDeScraper()
    broken_cars_mobile = mobile.search_broken_motors()
    functional_cars_mobile = mobile.search_functional_cars(min_price=10000)
    
    assert len(broken_cars_mobile) > 0, "Mobile.de should return broken cars"
    assert len(functional_cars_mobile) > 0, "Mobile.de should return functional cars"
    print(f"✓ MobileDeScraper: {len(broken_cars_mobile)} broken, {len(functional_cars_mobile)} functional")


def test_report_generator():
    """Test report generation."""
    print("\nTesting report generator...")
    
    # Setup logging
    logging.basicConfig(level=logging.WARNING)
    
    # Create test data
    broken_cars = [
        {'source': 'Test', 'make': 'BMW', 'model': '3 Series', 'year': 2015, 
         'price': 5000, 'mileage': 150000, 'condition': 'broken_motor', 'location': 'Berlin'}
    ]
    functional_cars = [
        {'source': 'Test', 'make': 'BMW', 'model': '3 Series', 'year': 2018,
         'price': 18000, 'mileage': 80000, 'condition': 'functional', 'location': 'Berlin'}
    ]
    
    # Generate reports in a test directory
    test_dir = Path('/tmp/test_reports')
    report_gen = CarReportGenerator(str(test_dir))
    report_gen.generate_reports(broken_cars, functional_cars)
    
    # Verify files were created
    assert (test_dir / 'broken_cars.csv').exists(), "broken_cars.csv should be created"
    assert (test_dir / 'functional_cars.csv').exists(), "functional_cars.csv should be created"
    assert (test_dir / 'comparison_summary.csv').exists(), "comparison_summary.csv should be created"
    
    print(f"✓ Reports generated successfully in {test_dir}")
    
    # Clean up
    import shutil
    shutil.rmtree(test_dir)
    print("✓ Test cleanup completed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running German Car Listings Analyzer Tests")
    print("=" * 60)
    
    try:
        test_scrapers()
        test_report_generator()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
