"""Simple test script to verify scraper implementations."""

import logging
import sys

from src.scraper import BaseScraper, AutoScout24Scraper, MobileScraper


def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def test_base_scraper():
    """Test that BaseScraper cannot be instantiated."""
    print("\n=== Testing BaseScraper ===")
    try:
        scraper = BaseScraper()
        print("ERROR: BaseScraper should not be instantiable (it's abstract)")
        return False
    except TypeError as e:
        print(f"✓ BaseScraper correctly raises TypeError: {e}")
        return True


def test_autoscout24_scraper():
    """Test AutoScout24Scraper initialization and methods."""
    print("\n=== Testing AutoScout24Scraper ===")
    try:
        scraper = AutoScout24Scraper()
        print(f"✓ AutoScout24Scraper initialized: {scraper.__class__.__name__}")
        
        # Check that methods exist and are callable
        assert hasattr(scraper, 'search_broken_motors'), "Missing search_broken_motors method"
        assert hasattr(scraper, 'search_functional_cars'), "Missing search_functional_cars method"
        assert callable(scraper.search_broken_motors), "search_broken_motors not callable"
        assert callable(scraper.search_functional_cars), "search_functional_cars not callable"
        print("✓ All required methods are present")
        
        # Check helper methods
        assert hasattr(scraper, '_load_user_agents'), "Missing _load_user_agents method"
        assert hasattr(scraper, '_implement_delay'), "Missing _implement_delay method"
        assert len(scraper.user_agents) > 0, "No user agents loaded"
        print(f"✓ Helper methods present, {len(scraper.user_agents)} user agents loaded")
        
        return True
    except Exception as e:
        print(f"✗ Error testing AutoScout24Scraper: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mobile_scraper():
    """Test MobileScraper initialization and methods."""
    print("\n=== Testing MobileScraper ===")
    try:
        scraper = MobileScraper()
        print(f"✓ MobileScraper initialized: {scraper.__class__.__name__}")
        
        # Check that methods exist and are callable
        assert hasattr(scraper, 'search_broken_motors'), "Missing search_broken_motors method"
        assert hasattr(scraper, 'search_functional_cars'), "Missing search_functional_cars method"
        assert callable(scraper.search_broken_motors), "search_broken_motors not callable"
        assert callable(scraper.search_functional_cars), "search_functional_cars not callable"
        print("✓ All required methods are present")
        
        # Check helper methods
        assert hasattr(scraper, '_load_user_agents'), "Missing _load_user_agents method"
        assert hasattr(scraper, '_implement_delay'), "Missing _implement_delay method"
        assert len(scraper.user_agents) > 0, "No user agents loaded"
        print(f"✓ Helper methods present, {len(scraper.user_agents)} user agents loaded")
        
        return True
    except Exception as e:
        print(f"✗ Error testing MobileScraper: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    setup_logging()
    
    print("=" * 60)
    print("Running Scraper Implementation Tests")
    print("=" * 60)
    
    results = {
        'BaseScraper': test_base_scraper(),
        'AutoScout24Scraper': test_autoscout24_scraper(),
        'MobileScraper': test_mobile_scraper(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
