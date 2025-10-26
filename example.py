"""Example script demonstrating the CSV Report Generator."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.csv_report import CarReportGenerator


def main():
    """Demonstrate the CSV report generator with sample data."""
    
    # Sample broken cars data
    broken_cars = [
        {
            'make': 'BMW',
            'model': '320i',
            'year': 2015,
            'price': 5000,
            'url': 'https://www.mobile.de/broken-bmw-320i'
        },
        {
            'make': 'Audi',
            'model': 'A4',
            'year': 2016,
            'price': 6000,
            'url': 'https://www.mobile.de/broken-audi-a4'
        },
        {
            'make': 'Mercedes',
            'model': 'C200',
            'year': 2014,
            'price': 4500,
            'url': 'https://www.mobile.de/broken-mercedes-c200'
        }
    ]
    
    # Sample functional cars data
    functional_cars = [
        {
            'make': 'BMW',
            'model': '320i',
            'year': 2015,
            'price': 12000,
            'mileage': 80000,
            'url': 'https://www.mobile.de/bmw-320i-1'
        },
        {
            'make': 'BMW',
            'model': '320i',
            'year': 2016,
            'price': 14000,
            'mileage': 60000,
            'url': 'https://www.mobile.de/bmw-320i-2'
        },
        {
            'make': 'BMW',
            'model': '320i',
            'year': 2015,
            'price': 11500,
            'mileage': 90000,
            'url': 'https://www.mobile.de/bmw-320i-3'
        },
        {
            'make': 'Audi',
            'model': 'A4',
            'year': 2016,
            'price': 15000,
            'mileage': 70000,
            'url': 'https://www.mobile.de/audi-a4-1'
        },
        {
            'make': 'Audi',
            'model': 'A4',
            'year': 2017,
            'price': 16500,
            'mileage': 50000,
            'url': 'https://www.mobile.de/audi-a4-2'
        }
    ]
    
    # Create report generator
    generator = CarReportGenerator(output_dir='reports')
    
    # Generate reports
    print("Generating CSV reports...")
    generator.generate_reports(broken_cars, functional_cars)
    
    print("\n✓ Reports generated successfully!")
    print("\nGenerated files:")
    print("  - reports/broken_cars_report.csv (main report)")
    print("  - reports/similar_cars_BMW_320i.csv")
    print("  - reports/similar_cars_Audi_A4.csv")
    print("\nNote: No similar cars found for Mercedes C200")


if __name__ == '__main__':
    main()
