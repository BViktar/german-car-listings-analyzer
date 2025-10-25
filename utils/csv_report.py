"""
CSV report generator for car listings analysis.
"""
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any


class CarReportGenerator:
    """
    Generator for car listing analysis reports.
    
    This class creates CSV reports comparing broken motor cars with functional cars,
    providing insights into price differences and potential savings.
    """
    
    def __init__(self, output_dir: str):
        """
        Initialize the report generator.
        
        Args:
            output_dir (str): Directory where reports will be saved.
        """
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(__name__)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"CarReportGenerator initialized with output directory: {self.output_dir}")
    
    def generate_reports(self, broken_cars: List[Dict[str, Any]], functional_cars: List[Dict[str, Any]]) -> None:
        """
        Generate comprehensive reports comparing broken and functional cars.
        
        Creates multiple CSV files:
        - broken_cars.csv: All broken motor listings
        - functional_cars.csv: All functional car listings
        - comparison_summary.csv: Summary statistics and comparisons
        
        Args:
            broken_cars (List[Dict[str, Any]]): List of broken motor car listings.
            functional_cars (List[Dict[str, Any]]): List of functional car listings.
        
        Raises:
            Exception: If there's an error generating the reports.
        """
        try:
            self.logger.info("Starting report generation...")
            
            # Generate individual reports
            self._generate_broken_cars_report(broken_cars)
            self._generate_functional_cars_report(functional_cars)
            self._generate_comparison_report(broken_cars, functional_cars)
            
            self.logger.info("All reports generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            raise
    
    def _generate_broken_cars_report(self, broken_cars: List[Dict[str, Any]]) -> None:
        """
        Generate CSV report for broken motor cars.
        
        Args:
            broken_cars (List[Dict[str, Any]]): List of broken motor car listings.
        """
        report_path = self.output_dir / 'broken_cars.csv'
        self.logger.info(f"Generating broken cars report: {report_path}")
        
        if not broken_cars:
            self.logger.warning("No broken cars data to report")
            return
        
        # Define CSV headers based on the keys in the first entry
        headers = list(broken_cars[0].keys())
        
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(broken_cars)
        
        self.logger.info(f"Broken cars report saved: {len(broken_cars)} entries")
    
    def _generate_functional_cars_report(self, functional_cars: List[Dict[str, Any]]) -> None:
        """
        Generate CSV report for functional cars.
        
        Args:
            functional_cars (List[Dict[str, Any]]): List of functional car listings.
        """
        report_path = self.output_dir / 'functional_cars.csv'
        self.logger.info(f"Generating functional cars report: {report_path}")
        
        if not functional_cars:
            self.logger.warning("No functional cars data to report")
            return
        
        # Define CSV headers based on the keys in the first entry
        headers = list(functional_cars[0].keys())
        
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(functional_cars)
        
        self.logger.info(f"Functional cars report saved: {len(functional_cars)} entries")
    
    def _generate_comparison_report(self, broken_cars: List[Dict[str, Any]], 
                                   functional_cars: List[Dict[str, Any]]) -> None:
        """
        Generate comparison summary report.
        
        Creates a summary comparing broken motor cars with functional cars,
        including average prices, price differences, and potential savings.
        
        Args:
            broken_cars (List[Dict[str, Any]]): List of broken motor car listings.
            functional_cars (List[Dict[str, Any]]): List of functional car listings.
        """
        report_path = self.output_dir / 'comparison_summary.csv'
        self.logger.info(f"Generating comparison report: {report_path}")
        
        # Calculate statistics
        broken_count = len(broken_cars)
        functional_count = len(functional_cars)
        
        broken_avg_price = sum(car['price'] for car in broken_cars) / broken_count if broken_count > 0 else 0
        functional_avg_price = sum(car['price'] for car in functional_cars) / functional_count if functional_count > 0 else 0
        
        broken_avg_mileage = sum(car['mileage'] for car in broken_cars) / broken_count if broken_count > 0 else 0
        functional_avg_mileage = sum(car['mileage'] for car in functional_cars) / functional_count if functional_count > 0 else 0
        
        price_difference = functional_avg_price - broken_avg_price
        
        # Prepare comparison data
        comparison_data = [
            {
                'metric': 'Total Broken Cars',
                'value': broken_count
            },
            {
                'metric': 'Total Functional Cars',
                'value': functional_count
            },
            {
                'metric': 'Average Price - Broken Cars (EUR)',
                'value': f'{broken_avg_price:.2f}'
            },
            {
                'metric': 'Average Price - Functional Cars (EUR)',
                'value': f'{functional_avg_price:.2f}'
            },
            {
                'metric': 'Average Mileage - Broken Cars (km)',
                'value': f'{broken_avg_mileage:.0f}'
            },
            {
                'metric': 'Average Mileage - Functional Cars (km)',
                'value': f'{functional_avg_mileage:.0f}'
            },
            {
                'metric': 'Price Difference (Functional - Broken) (EUR)',
                'value': f'{price_difference:.2f}'
            },
            {
                'metric': 'Potential Savings Percentage',
                'value': f'{(price_difference / functional_avg_price * 100):.2f}%' if functional_avg_price > 0 else 'N/A'
            }
        ]
        
        # Write comparison report
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['metric', 'value'])
            writer.writeheader()
            writer.writerows(comparison_data)
        
        self.logger.info("Comparison report saved")
