"""Data processing and analysis module."""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Handles data cleaning, processing, and analysis of car listings.
    
    Provides methods for cleaning scraped data, comparing prices,
    and generating statistical analysis.
    """
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.broken_motors_df: Optional[pd.DataFrame] = None
        self.functional_motors_df: Optional[pd.DataFrame] = None
        self.comparison_df: Optional[pd.DataFrame] = None
    
    def load_data(
        self,
        broken_motors_data: List[Dict[str, Any]],
        functional_motors_data: List[Dict[str, Any]],
    ) -> None:
        """
        Load raw data into DataFrames.
        
        Args:
            broken_motors_data: List of broken motor listings
            functional_motors_data: List of functional motor listings
        """
        logger.info("Loading data into DataFrames...")
        
        self.broken_motors_df = pd.DataFrame(broken_motors_data)
        self.functional_motors_df = pd.DataFrame(functional_motors_data)
        
        logger.info(f"Loaded {len(self.broken_motors_df)} broken motor listings")
        logger.info(f"Loaded {len(self.functional_motors_df)} functional motor listings")
    
    def clean_data(self) -> None:
        """
        Clean and standardize the loaded data.
        
        Removes duplicates, handles missing values, and standardizes formats.
        """
        logger.info("Cleaning data...")
        
        if self.broken_motors_df is not None:
            self.broken_motors_df = self._clean_dataframe(self.broken_motors_df)
            logger.info(f"Cleaned broken motors: {len(self.broken_motors_df)} records")
        
        if self.functional_motors_df is not None:
            self.functional_motors_df = self._clean_dataframe(self.functional_motors_df)
            logger.info(f"Cleaned functional motors: {len(self.functional_motors_df)} records")
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean a single DataFrame.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates based on URL
        if 'url' in df.columns:
            df = df.drop_duplicates(subset=['url'], keep='first')
        
        # Remove rows with missing critical data
        critical_columns = ['price', 'title']
        for col in critical_columns:
            if col in df.columns:
                df = df[df[col].notna()]
        
        # Convert numeric columns
        numeric_columns = ['price', 'year', 'mileage', 'horsepower']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove outliers in price (values that are clearly errors)
        if 'price' in df.columns:
            # Remove prices less than 100 or greater than 1,000,000
            df = df[(df['price'] >= 100) & (df['price'] <= 1000000)]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
    
    def analyze(self) -> pd.DataFrame:
        """
        Perform comparison analysis between broken and functional motors.
        
        Returns:
            DataFrame with comparison analysis
        """
        logger.info("Performing analysis...")
        
        if self.broken_motors_df is None or self.functional_motors_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        comparison_data = []
        
        # Overall price comparison
        broken_avg_price = self.broken_motors_df['price'].mean()
        functional_avg_price = self.functional_motors_df['price'].mean()
        
        comparison_data.append({
            'Category': 'Overall',
            'Broken Avg Price (€)': f"{broken_avg_price:,.2f}",
            'Functional Avg Price (€)': f"{functional_avg_price:,.2f}",
            'Price Difference (€)': f"{functional_avg_price - broken_avg_price:,.2f}",
            'Discount (%)': f"{(1 - broken_avg_price/functional_avg_price) * 100:.1f}%",
            'Broken Count': len(self.broken_motors_df),
            'Functional Count': len(self.functional_motors_df),
        })
        
        # Analysis by year
        if 'year' in self.broken_motors_df.columns and 'year' in self.functional_motors_df.columns:
            year_analysis = self._analyze_by_category('year')
            comparison_data.extend(year_analysis)
        
        # Analysis by fuel type
        if 'fuel_type' in self.broken_motors_df.columns and 'fuel_type' in self.functional_motors_df.columns:
            fuel_analysis = self._analyze_by_category('fuel_type')
            comparison_data.extend(fuel_analysis)
        
        # Analysis by transmission
        if 'transmission' in self.broken_motors_df.columns and 'transmission' in self.functional_motors_df.columns:
            transmission_analysis = self._analyze_by_category('transmission')
            comparison_data.extend(transmission_analysis)
        
        self.comparison_df = pd.DataFrame(comparison_data)
        
        logger.info("Analysis completed")
        return self.comparison_df
    
    def _analyze_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Analyze data grouped by a specific category.
        
        Args:
            category: Column name to group by
            
        Returns:
            List of comparison dictionaries
        """
        results = []
        
        # Get unique values from both datasets
        broken_values = set(self.broken_motors_df[category].dropna().unique())
        functional_values = set(self.functional_motors_df[category].dropna().unique())
        all_values = broken_values.union(functional_values)
        
        for value in sorted(all_values, key=str):
            broken_subset = self.broken_motors_df[self.broken_motors_df[category] == value]
            functional_subset = self.functional_motors_df[self.functional_motors_df[category] == value]
            
            if len(broken_subset) > 0 and len(functional_subset) > 0:
                broken_avg = broken_subset['price'].mean()
                functional_avg = functional_subset['price'].mean()
                
                results.append({
                    'Category': f"{category.replace('_', ' ').title()}: {value}",
                    'Broken Avg Price (€)': f"{broken_avg:,.2f}",
                    'Functional Avg Price (€)': f"{functional_avg:,.2f}",
                    'Price Difference (€)': f"{functional_avg - broken_avg:,.2f}",
                    'Discount (%)': f"{(1 - broken_avg/functional_avg) * 100:.1f}%",
                    'Broken Count': len(broken_subset),
                    'Functional Count': len(functional_subset),
                })
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get detailed statistics for both datasets.
        
        Returns:
            Dictionary containing statistical summaries
        """
        stats = {}
        
        if self.broken_motors_df is not None:
            stats['broken_motors'] = self._get_dataframe_stats(self.broken_motors_df)
        
        if self.functional_motors_df is not None:
            stats['functional_motors'] = self._get_dataframe_stats(self.functional_motors_df)
        
        return stats
    
    def _get_dataframe_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get statistics for a DataFrame.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary of statistics
        """
        stats = {
            'total_count': len(df),
        }
        
        # Price statistics
        if 'price' in df.columns:
            stats['price'] = {
                'mean': df['price'].mean(),
                'median': df['price'].median(),
                'std': df['price'].std(),
                'min': df['price'].min(),
                'max': df['price'].max(),
            }
        
        # Mileage statistics
        if 'mileage' in df.columns:
            stats['mileage'] = {
                'mean': df['mileage'].mean(),
                'median': df['mileage'].median(),
                'min': df['mileage'].min(),
                'max': df['mileage'].max(),
            }
        
        # Year statistics
        if 'year' in df.columns:
            stats['year'] = {
                'mean': df['year'].mean(),
                'median': df['year'].median(),
                'min': df['year'].min(),
                'max': df['year'].max(),
            }
        
        return stats
    
    def get_dataframes(self) -> tuple:
        """
        Get the processed DataFrames.
        
        Returns:
            Tuple of (broken_motors_df, functional_motors_df, comparison_df)
        """
        return self.broken_motors_df, self.functional_motors_df, self.comparison_df
