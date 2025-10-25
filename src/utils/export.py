"""Data export utilities for various output formats."""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src.config import OUTPUT_FILES

logger = logging.getLogger(__name__)


class DataExporter:
    """
    Handles exporting data to various formats (CSV, Excel, visualizations).
    """
    
    @staticmethod
    def to_csv(data: pd.DataFrame, filepath: Path, index: bool = False) -> None:
        """
        Export DataFrame to CSV file.
        
        Args:
            data: DataFrame to export
            filepath: Output file path
            index: Whether to include index in output
        """
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            data.to_csv(filepath, index=index, encoding='utf-8-sig')
            logger.info(f"Data exported to CSV: {filepath}")
        except Exception as e:
            logger.error(f"Failed to export to CSV: {e}")
            raise
    
    @staticmethod
    def to_excel(
        data: Dict[str, pd.DataFrame],
        filepath: Path,
        index: bool = False,
    ) -> None:
        """
        Export multiple DataFrames to Excel file with separate sheets.
        
        Args:
            data: Dictionary mapping sheet names to DataFrames
            filepath: Output file path
            index: Whether to include index in output
        """
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=index)
            
            logger.info(f"Data exported to Excel: {filepath}")
        except Exception as e:
            logger.error(f"Failed to export to Excel: {e}")
            raise
    
    @staticmethod
    def create_summary_table(
        broken_motors_df: pd.DataFrame,
        functional_motors_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create a summary comparison table.
        
        Args:
            broken_motors_df: DataFrame with broken motor listings
            functional_motors_df: DataFrame with functional motor listings
            
        Returns:
            Summary DataFrame with comparison statistics
        """
        summary_data = []
        
        # Price statistics
        summary_data.append({
            'Metric': 'Average Price',
            'Broken Motors': f"€{broken_motors_df['price'].mean():,.2f}" if 'price' in broken_motors_df.columns else 'N/A',
            'Functional Motors': f"€{functional_motors_df['price'].mean():,.2f}" if 'price' in functional_motors_df.columns else 'N/A',
        })
        
        summary_data.append({
            'Metric': 'Median Price',
            'Broken Motors': f"€{broken_motors_df['price'].median():,.2f}" if 'price' in broken_motors_df.columns else 'N/A',
            'Functional Motors': f"€{functional_motors_df['price'].median():,.2f}" if 'price' in functional_motors_df.columns else 'N/A',
        })
        
        summary_data.append({
            'Metric': 'Min Price',
            'Broken Motors': f"€{broken_motors_df['price'].min():,.2f}" if 'price' in broken_motors_df.columns else 'N/A',
            'Functional Motors': f"€{functional_motors_df['price'].min():,.2f}" if 'price' in functional_motors_df.columns else 'N/A',
        })
        
        summary_data.append({
            'Metric': 'Max Price',
            'Broken Motors': f"€{broken_motors_df['price'].max():,.2f}" if 'price' in broken_motors_df.columns else 'N/A',
            'Functional Motors': f"€{functional_motors_df['price'].max():,.2f}" if 'price' in functional_motors_df.columns else 'N/A',
        })
        
        # Count statistics
        summary_data.append({
            'Metric': 'Total Listings',
            'Broken Motors': len(broken_motors_df),
            'Functional Motors': len(functional_motors_df),
        })
        
        # Mileage statistics
        if 'mileage' in broken_motors_df.columns and 'mileage' in functional_motors_df.columns:
            summary_data.append({
                'Metric': 'Average Mileage (km)',
                'Broken Motors': f"{broken_motors_df['mileage'].mean():,.0f}",
                'Functional Motors': f"{functional_motors_df['mileage'].mean():,.0f}",
            })
        
        # Year statistics
        if 'year' in broken_motors_df.columns and 'year' in functional_motors_df.columns:
            summary_data.append({
                'Metric': 'Average Year',
                'Broken Motors': f"{broken_motors_df['year'].mean():.0f}",
                'Functional Motors': f"{functional_motors_df['year'].mean():.0f}",
            })
        
        return pd.DataFrame(summary_data)
    
    @staticmethod
    def create_price_comparison_chart(
        broken_motors_df: pd.DataFrame,
        functional_motors_df: pd.DataFrame,
        output_path: Optional[Path] = None,
    ) -> None:
        """
        Create a price comparison visualization.
        
        Args:
            broken_motors_df: DataFrame with broken motor listings
            functional_motors_df: DataFrame with functional motor listings
            output_path: Output file path for the chart
        """
        if output_path is None:
            output_path = OUTPUT_FILES['price_chart']
        
        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Box plot comparison
            data_to_plot = [
                broken_motors_df['price'].dropna(),
                functional_motors_df['price'].dropna()
            ]
            
            axes[0].boxplot(data_to_plot, labels=['Broken Motors', 'Functional Motors'])
            axes[0].set_title('Price Distribution Comparison')
            axes[0].set_ylabel('Price (€)')
            axes[0].grid(True, alpha=0.3)
            
            # Histogram comparison
            axes[1].hist(
                broken_motors_df['price'].dropna(),
                bins=30,
                alpha=0.6,
                label='Broken Motors',
                color='red'
            )
            axes[1].hist(
                functional_motors_df['price'].dropna(),
                bins=30,
                alpha=0.6,
                label='Functional Motors',
                color='green'
            )
            axes[1].set_title('Price Frequency Distribution')
            axes[1].set_xlabel('Price (€)')
            axes[1].set_ylabel('Frequency')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Price comparison chart saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to create price comparison chart: {e}")
            raise
    
    @staticmethod
    def generate_full_report(
        broken_motors_df: pd.DataFrame,
        functional_motors_df: pd.DataFrame,
        comparison_df: pd.DataFrame,
    ) -> None:
        """
        Generate a full analysis report with all outputs.
        
        Args:
            broken_motors_df: DataFrame with broken motor listings
            functional_motors_df: DataFrame with functional motor listings
            comparison_df: DataFrame with comparison analysis
        """
        logger.info("Generating full analysis report...")
        
        # Export to CSV
        DataExporter.to_csv(
            broken_motors_df,
            OUTPUT_FILES['broken_motors_csv']
        )
        DataExporter.to_csv(
            functional_motors_df,
            OUTPUT_FILES['functional_motors_csv']
        )
        DataExporter.to_csv(
            comparison_df,
            OUTPUT_FILES['comparison_csv']
        )
        
        # Create summary table
        summary_df = DataExporter.create_summary_table(
            broken_motors_df,
            functional_motors_df
        )
        
        # Export to Excel with multiple sheets
        excel_data = {
            'Summary': summary_df,
            'Broken Motors': broken_motors_df,
            'Functional Motors': functional_motors_df,
            'Comparison': comparison_df,
        }
        DataExporter.to_excel(excel_data, OUTPUT_FILES['summary_excel'])
        
        # Create visualizations
        if 'price' in broken_motors_df.columns and 'price' in functional_motors_df.columns:
            DataExporter.create_price_comparison_chart(
                broken_motors_df,
                functional_motors_df
            )
        
        logger.info("Full analysis report generated successfully")
