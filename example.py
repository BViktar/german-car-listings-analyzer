"""Example usage of the CarComparisonAnalyzer."""

from src.analysis.comparison_analyzer import CarComparisonAnalyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Sample data
broken_cars = [
    {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 5000, 'mileage': 120000},
    {'make': 'BMW', 'model': '320i', 'year': 2016, 'price': 6000, 'mileage': 100000},
    {'make': 'Audi', 'model': 'A4', 'year': 2014, 'price': 4500, 'mileage': 150000},
    {'make': 'Mercedes', 'model': 'C200', 'year': 2015, 'price': 7000, 'mileage': 110000},
]

functional_cars = [
    {'make': 'BMW', 'model': '320i', 'year': 2015, 'price': 15000, 'mileage': 80000},
    {'make': 'BMW', 'model': '320i', 'year': 2016, 'price': 18000, 'mileage': 60000},
    {'make': 'Audi', 'model': 'A4', 'year': 2014, 'price': 12000, 'mileage': 90000},
    {'make': 'Mercedes', 'model': 'C200', 'year': 2015, 'price': 20000, 'mileage': 70000},
    {'make': 'VW', 'model': 'Golf', 'year': 2017, 'price': 13000, 'mileage': 50000},
]

# Create analyzer and perform analysis
analyzer = CarComparisonAnalyzer()
result = analyzer.analyze_listings(broken_cars, functional_cars)

# Print summary
print("\n=== Car Comparison Analysis Summary ===\n")
print(f"Total broken cars: {result.summary['total_listings']['broken']}")
print(f"Total functional cars: {result.summary['total_listings']['functional']}")
print(f"\nAverage price difference: €{result.summary['average_price_difference']:.2f}")
print(f"Median price difference: €{result.summary['median_price_difference']:.2f}")

print("\n=== Price Analysis ===")
print(f"Broken cars - Mean: €{result.price_comparison['broken']['mean']:.2f}, "
      f"Median: €{result.price_comparison['broken']['median']:.2f}")
print(f"Functional cars - Mean: €{result.price_comparison['functional']['mean']:.2f}, "
      f"Median: €{result.price_comparison['functional']['median']:.2f}")

print("\n=== Mileage Analysis ===")
print(f"Broken cars - Mean: {result.mileage_analysis['broken']['mean']:.0f} km, "
      f"Median: {result.mileage_analysis['broken']['median']:.0f} km")
print(f"Functional cars - Mean: {result.mileage_analysis['functional']['mean']:.0f} km, "
      f"Median: {result.mileage_analysis['functional']['median']:.0f} km")

print("\n=== Age Analysis ===")
print(f"Broken cars - Mean age: {result.age_distribution['broken']['mean_age']:.1f} years")
print(f"Functional cars - Mean age: {result.age_distribution['functional']['mean_age']:.1f} years")

print("\n=== Model Statistics ===")
for model_key, stats in result.model_statistics.items():
    print(f"\n{model_key.replace('_', ' ')}:")
    print(f"  Broken: {stats['broken']['count']} cars, Avg price: €{stats['broken']['avg_price']:.2f}")
    print(f"  Functional: {stats['functional']['count']} cars, Avg price: €{stats['functional']['avg_price']:.2f}")

print("\n=== Most Common Makes ===")
print("Broken cars:", result.summary['most_common_makes']['broken'])
print("Functional cars:", result.summary['most_common_makes']['functional'])
