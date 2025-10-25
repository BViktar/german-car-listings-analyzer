"""Unit tests for the car comparison analyzer."""

import unittest
import pandas as pd
import numpy as np
from src.analysis.comparison_analyzer import CarComparisonAnalyzer, ComparisonResult


class TestCarComparisonAnalyzer(unittest.TestCase):
    """Test cases for CarComparisonAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CarComparisonAnalyzer()
        
        # Sample broken cars data
        self.broken_cars = [
            {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 5000, 'mileage': 120000},
            {'make': 'BMW', 'model': '320i', 'year': 2016, 'price': 6000, 'mileage': 100000},
            {'make': 'Audi', 'model': 'A4', 'year': 2014, 'price': 4500, 'mileage': 150000},
            {'make': 'Mercedes', 'model': 'C200', 'year': 2015, 'price': 7000, 'mileage': 110000},
        ]
        
        # Sample functional cars data
        self.functional_cars = [
            {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 15000, 'mileage': 80000},
            {'make': 'BMW', 'model': '320i', 'year': 2016, 'price': 18000, 'mileage': 60000},
            {'make': 'Audi', 'model': 'A4', 'year': 2014, 'price': 12000, 'mileage': 90000},
            {'make': 'Mercedes', 'model': 'C200', 'year': 2015, 'price': 20000, 'mileage': 70000},
            {'make': 'VW', 'model': 'Golf', 'year': 2017, 'price': 13000, 'mileage': 50000},
        ]
    
    def test_analyze_listings_returns_comparison_result(self):
        """Test that analyze_listings returns a ComparisonResult object."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        self.assertIsInstance(result, ComparisonResult)
        self.assertIsNotNone(result.price_comparison)
        self.assertIsNotNone(result.age_distribution)
        self.assertIsNotNone(result.mileage_analysis)
        self.assertIsNotNone(result.model_statistics)
        self.assertIsNotNone(result.summary)
    
    def test_price_comparison_structure(self):
        """Test that price comparison has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check broken cars price analysis
        self.assertIn('broken', result.price_comparison)
        self.assertIn('mean', result.price_comparison['broken'])
        self.assertIn('median', result.price_comparison['broken'])
        self.assertIn('std', result.price_comparison['broken'])
        self.assertIn('distribution', result.price_comparison['broken'])
        
        # Check functional cars price analysis
        self.assertIn('functional', result.price_comparison)
        self.assertIn('mean', result.price_comparison['functional'])
        self.assertIn('median', result.price_comparison['functional'])
        self.assertIn('std', result.price_comparison['functional'])
        self.assertIn('distribution', result.price_comparison['functional'])
        
        # Check by_model analysis
        self.assertIn('by_model', result.price_comparison)
    
    def test_price_analysis_calculations(self):
        """Test that price analysis calculations are correct."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Test broken cars mean price
        expected_broken_mean = sum([car['price'] for car in self.broken_cars]) / len(self.broken_cars)
        self.assertAlmostEqual(result.price_comparison['broken']['mean'], expected_broken_mean)
        
        # Test functional cars mean price
        expected_functional_mean = sum([car['price'] for car in self.functional_cars]) / len(self.functional_cars)
        self.assertAlmostEqual(result.price_comparison['functional']['mean'], expected_functional_mean)
    
    def test_age_distribution_structure(self):
        """Test that age distribution has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        self.assertIn('broken', result.age_distribution)
        self.assertIn('mean_age', result.age_distribution['broken'])
        self.assertIn('age_distribution', result.age_distribution['broken'])
        
        self.assertIn('functional', result.age_distribution)
        self.assertIn('mean_age', result.age_distribution['functional'])
        self.assertIn('age_distribution', result.age_distribution['functional'])
    
    def test_mileage_analysis_structure(self):
        """Test that mileage analysis has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check broken cars mileage analysis
        self.assertIn('broken', result.mileage_analysis)
        self.assertIn('mean', result.mileage_analysis['broken'])
        self.assertIn('median', result.mileage_analysis['broken'])
        self.assertIn('distribution', result.mileage_analysis['broken'])
        
        # Check functional cars mileage analysis
        self.assertIn('functional', result.mileage_analysis)
        self.assertIn('mean', result.mileage_analysis['functional'])
        self.assertIn('median', result.mileage_analysis['functional'])
        self.assertIn('distribution', result.mileage_analysis['functional'])
    
    def test_mileage_analysis_calculations(self):
        """Test that mileage analysis calculations are correct."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Test broken cars mean mileage
        expected_broken_mean = sum([car['mileage'] for car in self.broken_cars]) / len(self.broken_cars)
        self.assertAlmostEqual(result.mileage_analysis['broken']['mean'], expected_broken_mean)
        
        # Test functional cars mean mileage
        expected_functional_mean = sum([car['mileage'] for car in self.functional_cars]) / len(self.functional_cars)
        self.assertAlmostEqual(result.mileage_analysis['functional']['mean'], expected_functional_mean)
    
    def test_model_statistics_structure(self):
        """Test that model statistics has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check that BMW_320i is in the results
        self.assertIn('BMW_320i', result.model_statistics)
        
        # Check structure of model statistics
        bmw_stats = result.model_statistics['BMW_320i']
        self.assertIn('broken', bmw_stats)
        self.assertIn('functional', bmw_stats)
        
        # Check broken stats
        self.assertIn('count', bmw_stats['broken'])
        self.assertIn('avg_price', bmw_stats['broken'])
        self.assertIn('avg_mileage', bmw_stats['broken'])
        
        # Check functional stats
        self.assertIn('count', bmw_stats['functional'])
        self.assertIn('avg_price', bmw_stats['functional'])
        self.assertIn('avg_mileage', bmw_stats['functional'])
    
    def test_model_statistics_calculations(self):
        """Test that model statistics calculations are correct."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check BMW 320i broken car count
        bmw_broken_count = sum(1 for car in self.broken_cars if car['make'] == 'BMW' and car['model'] == '320i')
        self.assertEqual(result.model_statistics['BMW_320i']['broken']['count'], bmw_broken_count)
        
        # Check BMW 320i functional car count
        bmw_functional_count = sum(1 for car in self.functional_cars if car['make'] == 'BMW' and car['model'] == '320i')
        self.assertEqual(result.model_statistics['BMW_320i']['functional']['count'], bmw_functional_count)
    
    def test_summary_structure(self):
        """Test that summary has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        self.assertIn('total_listings', result.summary)
        self.assertIn('broken', result.summary['total_listings'])
        self.assertIn('functional', result.summary['total_listings'])
        
        self.assertIn('average_price_difference', result.summary)
        self.assertIn('median_price_difference', result.summary)
        self.assertIn('most_common_makes', result.summary)
        self.assertIn('broken', result.summary['most_common_makes'])
        self.assertIn('functional', result.summary['most_common_makes'])
    
    def test_summary_calculations(self):
        """Test that summary calculations are correct."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check total listings counts
        self.assertEqual(result.summary['total_listings']['broken'], len(self.broken_cars))
        self.assertEqual(result.summary['total_listings']['functional'], len(self.functional_cars))
        
        # Check price differences
        broken_mean = sum([car['price'] for car in self.broken_cars]) / len(self.broken_cars)
        functional_mean = sum([car['price'] for car in self.functional_cars]) / len(self.functional_cars)
        expected_diff = functional_mean - broken_mean
        self.assertAlmostEqual(result.summary['average_price_difference'], expected_diff)
    
    def test_prices_by_model_structure(self):
        """Test that prices by model has the correct structure."""
        result = self.analyzer.analyze_listings(self.broken_cars, self.functional_cars)
        
        # Check that BMW_320i is in the by_model results
        self.assertIn('BMW_320i', result.price_comparison['by_model'])
        
        bmw_price_diff = result.price_comparison['by_model']['BMW_320i']
        self.assertIn('price_difference', bmw_price_diff)
        self.assertIn('mean', bmw_price_diff['price_difference'])
        self.assertIn('median', bmw_price_diff['price_difference'])
        self.assertIn('sample_sizes', bmw_price_diff)
        self.assertIn('broken', bmw_price_diff['sample_sizes'])
        self.assertIn('functional', bmw_price_diff['sample_sizes'])
    
    def test_empty_lists_handling(self):
        """Test that analyzer handles empty lists gracefully."""
        # Empty broken cars should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.analyzer.analyze_listings([], self.functional_cars)
        self.assertIn("broken_cars list cannot be empty", str(context.exception))
        
        # Empty functional cars should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.analyzer.analyze_listings(self.broken_cars, [])
        self.assertIn("functional_cars list cannot be empty", str(context.exception))
    
    def test_invalid_input_types(self):
        """Test that analyzer handles invalid input types."""
        # Non-list input should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.analyzer.analyze_listings("not a list", self.functional_cars)
        self.assertIn("must be lists", str(context.exception))
        
        # Non-dict items in list should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.analyzer.analyze_listings([1, 2, 3], self.functional_cars)
        self.assertIn("must be dictionaries", str(context.exception))
    
    def test_missing_required_columns(self):
        """Test that analyzer validates required columns."""
        # Missing 'price' column
        broken_incomplete = [{'make': 'BMW', 'model': '320i', 'year': 2015, 'mileage': 120000}]
        
        with self.assertRaises(KeyError) as context:
            self.analyzer.analyze_listings(broken_incomplete, self.functional_cars)
        self.assertIn("Missing required columns", str(context.exception))
        self.assertIn("price", str(context.exception))
    
    
    def test_single_car_lists(self):
        """Test that analyzer works with single car in each list."""
        broken = [{'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 5000, 'mileage': 120000}]
        functional = [{'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 15000, 'mileage': 80000}]
        
        result = self.analyzer.analyze_listings(broken, functional)
        
        self.assertIsInstance(result, ComparisonResult)
        self.assertEqual(result.summary['total_listings']['broken'], 1)
        self.assertEqual(result.summary['total_listings']['functional'], 1)


if __name__ == '__main__':
    unittest.main()
