"""Car comparison analyzer for comparing broken and functional cars."""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging


@dataclass
class ComparisonResult:
    """Data class for storing comparison results."""
    price_comparison: Dict
    age_distribution: Dict
    mileage_analysis: Dict
    model_statistics: Dict
    summary: Dict


class CarComparisonAnalyzer:
    """Analyzes and compares cars with broken motors against functional cars."""
    
    def __init__(self):
        """Initialize the CarComparisonAnalyzer with logging."""
        self.logger = logging.getLogger(__name__)
        
    def analyze_listings(self, broken_cars: List[Dict], functional_cars: List[Dict]) -> ComparisonResult:
        """
        Perform comprehensive analysis of car listings.
        
        Args:
            broken_cars: List of dictionaries containing broken car listings
            functional_cars: List of dictionaries containing functional car listings
            
        Returns:
            ComparisonResult containing all analysis results
            
        Raises:
            ValueError: If input data is invalid (empty lists, missing required columns)
            KeyError: If required columns are missing from the data
            Exception: If analysis fails for other reasons
        """
        try:
            # Validate input data
            self._validate_input(broken_cars, functional_cars)
            
            # Convert listings to DataFrames
            broken_df = pd.DataFrame(broken_cars)
            functional_df = pd.DataFrame(functional_cars)
            
            # Validate required columns
            self._validate_dataframes(broken_df, functional_df)
            
            # Perform analyses
            price_comparison = self._analyze_prices(broken_df, functional_df)
            age_distribution = self._analyze_age(broken_df, functional_df)
            mileage_analysis = self._analyze_mileage(broken_df, functional_df)
            model_statistics = self._analyze_models(broken_df, functional_df)
            summary = self._create_summary(broken_df, functional_df)
            
            return ComparisonResult(
                price_comparison=price_comparison,
                age_distribution=age_distribution,
                mileage_analysis=mileage_analysis,
                model_statistics=model_statistics,
                summary=summary
            )
            
        except (ValueError, KeyError) as e:
            self.logger.error(f"Data validation error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during analysis: {str(e)}")
            raise
    
    def _validate_input(self, broken_cars: List[Dict], functional_cars: List[Dict]) -> None:
        """
        Validate input data for analysis.
        
        Args:
            broken_cars: List of dictionaries containing broken car listings
            functional_cars: List of dictionaries containing functional car listings
            
        Raises:
            ValueError: If input data is invalid
        """
        if not broken_cars:
            raise ValueError("broken_cars list cannot be empty")
        
        if not functional_cars:
            raise ValueError("functional_cars list cannot be empty")
        
        if not isinstance(broken_cars, list) or not isinstance(functional_cars, list):
            raise ValueError("broken_cars and functional_cars must be lists")
        
        if not all(isinstance(car, dict) for car in broken_cars):
            raise ValueError("All items in broken_cars must be dictionaries")
        
        if not all(isinstance(car, dict) for car in functional_cars):
            raise ValueError("All items in functional_cars must be dictionaries")
    
    def _validate_dataframes(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> None:
        """
        Validate that DataFrames have required columns.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Raises:
            KeyError: If required columns are missing
        """
        required_columns = ['make', 'model', 'year', 'price', 'mileage']
        
        missing_broken = [col for col in required_columns if col not in broken_df.columns]
        if missing_broken:
            raise KeyError(f"Missing required columns in broken_cars: {missing_broken}")
        
        missing_functional = [col for col in required_columns if col not in functional_df.columns]
        if missing_functional:
            raise KeyError(f"Missing required columns in functional_cars: {missing_functional}")
            
    def _analyze_prices(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Analyze price distributions and differences.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing price analysis results
        """
        analysis = {
            'broken': {
                'mean': broken_df['price'].mean(),
                'median': broken_df['price'].median(),
                'std': broken_df['price'].std(),
                'distribution': broken_df['price'].to_list()
            },
            'functional': {
                'mean': functional_df['price'].mean(),
                'median': functional_df['price'].median(),
                'std': functional_df['price'].std(),
                'distribution': functional_df['price'].to_list()
            }
        }
        
        # Add model-specific price analysis
        analysis['by_model'] = self._analyze_prices_by_model(broken_df, functional_df)
        return analysis
        
    def _analyze_age(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Analyze age distributions.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing age analysis results
        """
        current_year = pd.Timestamp.now().year
        
        analysis = {
            'broken': {
                'mean_age': current_year - broken_df['year'].mean(),
                'age_distribution': (current_year - broken_df['year']).to_list()
            },
            'functional': {
                'mean_age': current_year - functional_df['year'].mean(),
                'age_distribution': (current_year - functional_df['year']).to_list()
            }
        }
        return analysis
        
    def _analyze_mileage(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Analyze mileage distributions.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing mileage analysis results
        """
        analysis = {
            'broken': {
                'mean': broken_df['mileage'].mean(),
                'median': broken_df['mileage'].median(),
                'distribution': broken_df['mileage'].to_list()
            },
            'functional': {
                'mean': functional_df['mileage'].mean(),
                'median': functional_df['mileage'].median(),
                'distribution': functional_df['mileage'].to_list()
            }
        }
        return analysis
        
    def _analyze_models(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Analyze statistics by make/model.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing model-specific statistics
        """
        analysis = {}
        
        # Group by make and model
        broken_grouped = broken_df.groupby(['make', 'model'])
        functional_grouped = functional_df.groupby(['make', 'model'])
        
        # Calculate statistics for each group
        for (make, model), group in broken_grouped:
            if (make, model) in functional_grouped.groups:
                functional_group = functional_grouped.get_group((make, model))
                
                analysis[f"{make}_{model}"] = {
                    'broken': {
                        'count': len(group),
                        'avg_price': group['price'].mean(),
                        'avg_mileage': group['mileage'].mean()
                    },
                    'functional': {
                        'count': len(functional_group),
                        'avg_price': functional_group['price'].mean(),
                        'avg_mileage': functional_group['mileage'].mean()
                    }
                }
                
        return analysis
        
    def _create_summary(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Create summary statistics.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing summary statistics
        """
        summary = {
            'total_listings': {
                'broken': len(broken_df),
                'functional': len(functional_df)
            },
            'average_price_difference': (
                functional_df['price'].mean() - broken_df['price'].mean()
            ),
            'median_price_difference': (
                functional_df['price'].median() - broken_df['price'].median()
            ),
            'most_common_makes': {
                'broken': broken_df['make'].value_counts().head().to_dict(),
                'functional': functional_df['make'].value_counts().head().to_dict()
            }
        }
        return summary
        
    def _analyze_prices_by_model(self, broken_df: pd.DataFrame, functional_df: pd.DataFrame) -> Dict:
        """
        Analyze price differences by model.
        
        Args:
            broken_df: DataFrame containing broken car listings
            functional_df: DataFrame containing functional car listings
            
        Returns:
            Dictionary containing model-specific price analysis
        """
        analysis = {}
        
        # Group by make and model
        broken_grouped = broken_df.groupby(['make', 'model'])['price']
        functional_grouped = functional_df.groupby(['make', 'model'])['price']
        
        # Calculate price differences
        for (make, model), prices in broken_grouped:
            if (make, model) in functional_grouped.groups:
                functional_prices = functional_grouped.get_group((make, model))
                
                analysis[f"{make}_{model}"] = {
                    'price_difference': {
                        'mean': functional_prices.mean() - prices.mean(),
                        'median': functional_prices.median() - prices.median()
                    },
                    'sample_sizes': {
                        'broken': len(prices),
                        'functional': len(functional_prices)
                    }
                }
                
        return analysis
