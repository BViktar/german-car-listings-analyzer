"""
Analyzer for car listings data.

This module provides statistical analysis and comparison functionality
for broken motor vehicles vs. functional ones.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple

try:
    import pandas as pd
    import numpy as np
except ImportError:
    # Dependencies will be installed via requirements.txt
    pass

from src.config import Config


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ListingAnalyzer:
    """Analyzer for car listing data."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the analyzer.
        
        Args:
            config: Optional configuration dictionary. Uses Config.ANALYSIS if not provided.
        """
        self.config = config or Config.ANALYSIS
    
    def create_dataframe(self, listings: List[Dict[str, Any]]) -> 'pd.DataFrame':
        """
        Convert listings to a pandas DataFrame.
        
        Args:
            listings: List of listing dictionaries
        
        Returns:
            DataFrame with listing data
        """
        if not listings:
            logger.warning("No listings provided to create DataFrame")
            return pd.DataFrame()
        
        return pd.DataFrame(listings)
    
    def calculate_price_statistics(self, df: 'pd.DataFrame', 
                                   price_column: str = 'price') -> Dict[str, float]:
        """
        Calculate price statistics for listings.
        
        Args:
            df: DataFrame with listing data
            price_column: Name of the price column
        
        Returns:
            Dictionary with statistical measures
        """
        if df.empty or price_column not in df.columns:
            return {}
        
        prices = df[price_column].dropna()
        
        if len(prices) == 0:
            return {}
        
        return {
            'mean': float(prices.mean()),
            'median': float(prices.median()),
            'std': float(prices.std()),
            'min': float(prices.min()),
            'max': float(prices.max()),
            'count': int(len(prices))
        }
    
    def compare_broken_vs_functional(self, 
                                    broken_listings: List[Dict[str, Any]],
                                    functional_listings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare price statistics between broken and functional vehicles.
        
        Args:
            broken_listings: List of listings with broken motors
            functional_listings: List of functional vehicle listings
        
        Returns:
            Dictionary with comparison results
        """
        broken_df = self.create_dataframe(broken_listings)
        functional_df = self.create_dataframe(functional_listings)
        
        broken_stats = self.calculate_price_statistics(broken_df)
        functional_stats = self.calculate_price_statistics(functional_df)
        
        comparison = {
            'broken': broken_stats,
            'functional': functional_stats,
            'difference': {}
        }
        
        # Calculate differences if both have data
        if broken_stats and functional_stats:
            comparison['difference'] = {
                'mean_diff': functional_stats['mean'] - broken_stats['mean'],
                'median_diff': functional_stats['median'] - broken_stats['median'],
                'mean_ratio': (functional_stats['mean'] / broken_stats['mean'] 
                              if broken_stats['mean'] > 0 else None)
            }
        
        return comparison
    
    def detect_outliers(self, df: 'pd.DataFrame', 
                       column: str = 'price') -> Tuple['pd.DataFrame', 'pd.DataFrame']:
        """
        Detect outliers using z-score method.
        
        Args:
            df: DataFrame with listing data
            column: Column to check for outliers
        
        Returns:
            Tuple of (outliers_df, clean_df)
        """
        if df.empty or column not in df.columns:
            return pd.DataFrame(), df
        
        values = df[column].dropna()
        
        if len(values) < self.config['min_sample_size']:
            logger.warning(f"Sample size ({len(values)}) below minimum ({self.config['min_sample_size']})")
            return pd.DataFrame(), df
        
        # Calculate z-scores
        mean = values.mean()
        std = values.std()
        
        if std == 0:
            return pd.DataFrame(), df
        
        z_scores = np.abs((values - mean) / std)
        threshold = self.config['outlier_threshold']
        
        # Identify outliers
        outlier_mask = z_scores > threshold
        outliers = df[df[column].notna()][outlier_mask]
        clean_data = df[df[column].notna()][~outlier_mask]
        
        logger.info(f"Detected {len(outliers)} outliers out of {len(values)} values")
        
        return outliers, clean_data
    
    def group_by_make_model(self, df: 'pd.DataFrame') -> Dict[str, 'pd.DataFrame']:
        """
        Group listings by make and model.
        
        Args:
            df: DataFrame with listing data
        
        Returns:
            Dictionary mapping (make, model) tuples to DataFrames
        """
        if df.empty:
            return {}
        
        required_columns = ['make', 'model']
        if not all(col in df.columns for col in required_columns):
            logger.warning("Make and/or model columns not found in DataFrame")
            return {}
        
        grouped = df.groupby(['make', 'model'])
        
        return {
            (make, model): group 
            for (make, model), group in grouped
        }
    
    def calculate_depreciation_rate(self, 
                                    broken_price: float, 
                                    functional_price: float) -> float:
        """
        Calculate depreciation rate for broken motor vehicles.
        
        Args:
            broken_price: Average price of broken motor vehicles
            functional_price: Average price of functional vehicles
        
        Returns:
            Depreciation rate as a percentage
        """
        if functional_price == 0:
            return 0.0
        
        depreciation = ((functional_price - broken_price) / functional_price) * 100
        return round(depreciation, 2)
    
    def generate_summary_report(self, 
                               broken_listings: List[Dict[str, Any]],
                               functional_listings: List[Dict[str, Any]]) -> str:
        """
        Generate a text summary report of the analysis.
        
        Args:
            broken_listings: List of listings with broken motors
            functional_listings: List of functional vehicle listings
        
        Returns:
            Formatted summary report as string
        """
        comparison = self.compare_broken_vs_functional(broken_listings, functional_listings)
        
        report = []
        report.append("=" * 60)
        report.append("Car Listings Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        # Broken vehicles section
        report.append("Broken Motor Vehicles:")
        if comparison['broken']:
            stats = comparison['broken']
            report.append(f"  Count: {stats['count']}")
            report.append(f"  Average Price: €{stats['mean']:,.2f}")
            report.append(f"  Median Price: €{stats['median']:,.2f}")
            report.append(f"  Price Range: €{stats['min']:,.2f} - €{stats['max']:,.2f}")
        else:
            report.append("  No data available")
        report.append("")
        
        # Functional vehicles section
        report.append("Functional Vehicles:")
        if comparison['functional']:
            stats = comparison['functional']
            report.append(f"  Count: {stats['count']}")
            report.append(f"  Average Price: €{stats['mean']:,.2f}")
            report.append(f"  Median Price: €{stats['median']:,.2f}")
            report.append(f"  Price Range: €{stats['min']:,.2f} - €{stats['max']:,.2f}")
        else:
            report.append("  No data available")
        report.append("")
        
        # Comparison section
        if comparison['difference']:
            diff = comparison['difference']
            report.append("Price Comparison:")
            report.append(f"  Mean Price Difference: €{diff['mean_diff']:,.2f}")
            report.append(f"  Median Price Difference: €{diff['median_diff']:,.2f}")
            if diff['mean_ratio']:
                report.append(f"  Price Ratio (Functional/Broken): {diff['mean_ratio']:.2f}x")
            
            if comparison['broken'] and comparison['functional']:
                depr_rate = self.calculate_depreciation_rate(
                    comparison['broken']['mean'],
                    comparison['functional']['mean']
                )
                report.append(f"  Depreciation Rate: {depr_rate}%")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
