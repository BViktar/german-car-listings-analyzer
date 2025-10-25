"""Example usage of the CarDataVisualizer."""

import logging
from src.utils.visualization import CarDataVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    """Demonstrate usage of CarDataVisualizer."""
    # Sample analysis data
    analysis_data = {
        'price_comparison': {
            'broken': [5000, 6000, 5500, 7000, 6500, 5800, 6200],
            'functional': [15000, 16000, 15500, 17000, 16500, 15800, 16200],
            'broken_avg': 6000,
            'functional_avg': 16000,
            'broken_median': 6000,
            'functional_median': 16000,
            'broken_min': 5000,
            'functional_min': 15000,
            'broken_max': 7000,
            'functional_max': 17000,
            'broken_std': 707.1,
            'functional_std': 707.1,
            'by_model': {
                'BMW 3 Series': {
                    'broken_avg': 5500,
                    'functional_avg': 15500
                },
                'Mercedes C-Class': {
                    'broken_avg': 6500,
                    'functional_avg': 16500
                },
                'Audi A4': {
                    'broken_avg': 6000,
                    'functional_avg': 16000
                }
            }
        },
        'age_distribution': {
            'broken': [5, 6, 7, 8, 9, 10, 7],
            'functional': [2, 3, 4, 5, 6, 3, 4],
            'broken_avg': 7.4,
            'functional_avg': 3.9,
            'broken_median': 7.0,
            'functional_median': 4.0,
            'broken_min': 5,
            'functional_min': 2,
            'broken_max': 10,
            'functional_max': 6,
            'broken_std': 1.58,
            'functional_std': 1.58
        },
        'mileage_analysis': {
            'broken': [100000, 120000, 110000, 130000, 115000, 125000, 105000],
            'functional': [50000, 60000, 55000, 65000, 58000, 52000, 61000],
            'broken_avg': 115000,
            'functional_avg': 57286,
            'broken_median': 115000,
            'functional_median': 58000,
            'broken_min': 100000,
            'functional_min': 50000,
            'broken_max': 130000,
            'functional_max': 65000,
            'broken_std': 11180,
            'functional_std': 5701
        },
        'model_statistics': {
            'BMW 3 Series': {
                'broken_count': 3,
                'functional_count': 5,
                'broken_avg_price': 5500,
                'functional_avg_price': 15500,
                'price_diff': 10000
            },
            'Mercedes C-Class': {
                'broken_count': 2,
                'functional_count': 4,
                'broken_avg_price': 6500,
                'functional_avg_price': 16500,
                'price_diff': 10000
            },
            'Audi A4': {
                'broken_count': 2,
                'functional_count': 3,
                'broken_avg_price': 6000,
                'functional_avg_price': 16000,
                'price_diff': 10000
            }
        },
        'summary': {
            'total_broken': 7,
            'total_functional': 12,
            'avg_price_diff': 10000,
            'avg_age_diff': 3.5,
            'avg_mileage_diff': 57714
        }
    }

    # Create visualizer instance
    visualizer = CarDataVisualizer(output_dir='output')

    # Generate visualizations
    print("Generating price comparison visualizations...")
    visualizer.create_price_comparison(analysis_data)

    print("Generating age distribution visualization...")
    visualizer.create_age_distribution(analysis_data)

    print("Generating mileage comparison visualization...")
    visualizer.create_mileage_comparison(analysis_data)

    # Export to Excel
    print("Exporting data to Excel...")
    visualizer.export_excel_report(analysis_data)

    print("\nAll visualizations and reports generated successfully!")
    print("Check the 'output' directory for results:")
    print("  - price_distribution.png")
    print("  - model_price_comparison.png")
    print("  - age_distribution.png")
    print("  - mileage_comparison.png")
    print("  - car_analysis.xlsx")


if __name__ == '__main__':
    main()
