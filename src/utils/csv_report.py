import csv
from pathlib import Path
from typing import Dict, List
import logging
import pandas as pd


class CarReportGenerator:
    """Generates CSV reports for car listings comparison."""
    
    def __init__(self, output_dir: str = 'reports'):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_reports(self, broken_cars: List[Dict], functional_cars: List[Dict]) -> None:
        """Generate main report and linked similar cars reports."""
        try:
            # Group functional cars by make and model
            functional_grouped = self._group_by_make_model(functional_cars)
            
            # Create main report
            main_report_path = self.output_dir / 'broken_cars_report.csv'
            self._generate_main_report(broken_cars, functional_grouped, main_report_path)
            
            # Create individual reports for similar cars
            self._generate_similar_cars_reports(functional_grouped)
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            raise
            
    def _generate_main_report(self, broken_cars: List[Dict], 
                            functional_grouped: Dict, 
                            output_path: Path) -> None:
        """Generate main report with broken cars and links to similar cars."""
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                    'car_description',
                    'advertisement_link',
                    'price',
                    'average_similar_price',
                    'similar_cars_file'
                ])
                writer.writeheader()
                
                for car in broken_cars:
                    make_model = f"{car['make']}_{car['model']}"
                    similar_cars = functional_grouped.get(make_model, [])
                    
                    similar_cars_file = f"similar_cars_{make_model}.csv"
                    avg_price = sum(c['price'] for c in similar_cars) / len(similar_cars) if similar_cars else 0
                    
                    writer.writerow({
                        'car_description': f"{car['year']} {car['make']} {car['model']}",
                        'advertisement_link': car['url'],
                        'price': car['price'],
                        'average_similar_price': round(avg_price, 2),
                        'similar_cars_file': similar_cars_file if similar_cars else ''
                    })
                    
        except Exception as e:
            self.logger.error(f"Error generating main report: {str(e)}")
            raise
            
    def _generate_similar_cars_reports(self, functional_grouped: Dict) -> None:
        """Generate individual reports for similar cars by make/model."""
        try:
            for make_model, cars in functional_grouped.items():
                output_path = self.output_dir / f"similar_cars_{make_model}.csv"
                
                with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=[
                        'make',
                        'model',
                        'year',
                        'price',
                        'mileage',
                        'url'
                    ])
                    writer.writeheader()
                    writer.writerows(cars)
                    
        except Exception as e:
            self.logger.error(f"Error generating similar cars reports: {str(e)}")
            raise
            
    def _group_by_make_model(self, cars: List[Dict]) -> Dict:
        """Group cars by make and model."""
        grouped = {}
        for car in cars:
            make_model = f"{car['make']}_{car['model']}"
            if make_model not in grouped:
                grouped[make_model] = []
            grouped[make_model].append(car)
        return grouped
