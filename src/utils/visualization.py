"""Visualization and reporting module for car data analysis."""

from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging


class CarDataVisualizer:
    """Generates visualizations and reports for car comparison analysis."""

    def __init__(self, output_dir: str = 'output'):
        """Initialize the visualizer with an output directory.

        Args:
            output_dir: Directory where visualizations and reports will be saved.
        """
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Set seaborn style for better-looking plots
        sns.set_style("whitegrid")

    def create_price_comparison(self, analysis: Dict) -> None:
        """Create price comparison visualizations.

        Args:
            analysis: Dictionary containing analysis data with 'price_comparison' key.
        """
        try:
            # Box plot of price distributions
            plt.figure(figsize=(10, 6))
            self._create_price_boxplot(analysis['price_comparison'])
            plt.savefig(
                self.output_dir / 'price_distribution.png',
                dpi=300,
                bbox_inches='tight'
            )
            plt.close()

            # Model-specific price comparisons
            plt.figure(figsize=(12, 8))
            self._create_model_price_comparison(analysis['price_comparison'])
            plt.savefig(
                self.output_dir / 'model_price_comparison.png',
                dpi=300,
                bbox_inches='tight'
            )
            plt.close()

            self.logger.info("Price comparison visualizations created successfully")

        except Exception as e:
            self.logger.error(f"Error creating price comparison: {str(e)}")
            raise

    def create_age_distribution(self, analysis: Dict) -> None:
        """Create age distribution visualizations.

        Args:
            analysis: Dictionary containing analysis data with 'age_distribution' key.
        """
        try:
            plt.figure(figsize=(10, 6))
            self._create_age_histogram(analysis['age_distribution'])
            plt.savefig(
                self.output_dir / 'age_distribution.png',
                dpi=300,
                bbox_inches='tight'
            )
            plt.close()

            self.logger.info("Age distribution visualization created successfully")

        except Exception as e:
            self.logger.error(f"Error creating age distribution: {str(e)}")
            raise

    def create_mileage_comparison(self, analysis: Dict) -> None:
        """Create mileage comparison visualizations.

        Args:
            analysis: Dictionary containing analysis data with 'mileage_analysis' key.
        """
        try:
            plt.figure(figsize=(10, 6))
            self._create_mileage_boxplot(analysis['mileage_analysis'])
            plt.savefig(
                self.output_dir / 'mileage_comparison.png',
                dpi=300,
                bbox_inches='tight'
            )
            plt.close()

            self.logger.info("Mileage comparison visualization created successfully")

        except Exception as e:
            self.logger.error(f"Error creating mileage comparison: {str(e)}")
            raise

    def export_excel_report(self, analysis: Dict) -> None:
        """Export detailed analysis to Excel.

        Args:
            analysis: Dictionary containing all analysis data.
        """
        try:
            # Check if we have any data to export
            has_data = any([
                analysis.get('price_comparison'),
                analysis.get('model_statistics'),
                analysis.get('mileage_analysis'),
                analysis.get('age_distribution'),
                analysis.get('summary')
            ])

            if not has_data:
                self.logger.warning("No data to export to Excel")
                # Create an empty Excel file with a placeholder sheet
                df = pd.DataFrame({'Message': ['No data available']})
                df.to_excel(
                    self.output_dir / 'car_analysis.xlsx',
                    sheet_name='Empty',
                    index=False
                )
                return

            with pd.ExcelWriter(
                self.output_dir / 'car_analysis.xlsx',
                engine='openpyxl'
            ) as writer:
                # Price analysis
                self._export_price_analysis(analysis['price_comparison'], writer)

                # Model statistics
                self._export_model_statistics(analysis['model_statistics'], writer)

                # Mileage analysis
                self._export_mileage_analysis(analysis['mileage_analysis'], writer)

                # Age distribution
                self._export_age_analysis(analysis['age_distribution'], writer)

                # Summary
                self._export_summary(analysis['summary'], writer)

            self.logger.info("Excel report exported successfully")

        except Exception as e:
            self.logger.error(f"Error exporting Excel report: {str(e)}")
            raise

    def _create_price_boxplot(self, price_data: Dict) -> None:
        """Create box plot comparing price distributions.

        Args:
            price_data: Dictionary containing price data with 'broken' and 'functional' keys.
        """
        if not price_data or 'broken' not in price_data or 'functional' not in price_data:
            self.logger.warning("Insufficient price data for boxplot")
            return

        data = []
        labels = []

        if price_data['broken']:
            data.append(price_data['broken'])
            labels.append('Broken Motor')

        if price_data['functional']:
            data.append(price_data['functional'])
            labels.append('Functional')

        if data:
            plt.boxplot(data, tick_labels=labels)
            plt.ylabel('Price (€)')
            plt.title('Price Distribution: Broken vs Functional Cars')
            plt.grid(True, alpha=0.3)

    def _create_model_price_comparison(self, price_data: Dict) -> None:
        """Create bar chart comparing prices by model.

        Args:
            price_data: Dictionary containing price data by model.
        """
        if not price_data or 'by_model' not in price_data:
            self.logger.warning("No model-specific price data available")
            return

        models = []
        broken_prices = []
        functional_prices = []

        for model, data in price_data['by_model'].items():
            models.append(model)
            broken_prices.append(data.get('broken_avg', 0))
            functional_prices.append(data.get('functional_avg', 0))

        if models:
            x = range(len(models))
            width = 0.35

            plt.bar(
                [i - width / 2 for i in x],
                broken_prices,
                width,
                label='Broken Motor',
                alpha=0.8
            )
            plt.bar(
                [i + width / 2 for i in x],
                functional_prices,
                width,
                label='Functional',
                alpha=0.8
            )

            plt.xlabel('Car Model')
            plt.ylabel('Average Price (€)')
            plt.title('Average Price Comparison by Model')
            plt.xticks(x, models, rotation=45, ha='right')
            plt.legend()
            plt.grid(True, alpha=0.3, axis='y')

    def _create_age_histogram(self, age_data: Dict) -> None:
        """Create histogram of age distributions.

        Args:
            age_data: Dictionary containing age data with 'broken' and 'functional' keys.
        """
        if not age_data or 'broken' not in age_data or 'functional' not in age_data:
            self.logger.warning("Insufficient age data for histogram")
            return

        has_data = False

        if age_data['broken']:
            plt.hist(
                age_data['broken'],
                bins=20,
                alpha=0.5,
                label='Broken Motor',
                edgecolor='black'
            )
            has_data = True

        if age_data['functional']:
            plt.hist(
                age_data['functional'],
                bins=20,
                alpha=0.5,
                label='Functional',
                edgecolor='black'
            )
            has_data = True

        plt.xlabel('Age (years)')
        plt.ylabel('Frequency')
        plt.title('Age Distribution: Broken vs Functional Cars')

        if has_data:
            plt.legend()

        plt.grid(True, alpha=0.3)

    def _create_mileage_boxplot(self, mileage_data: Dict) -> None:
        """Create box plot comparing mileage distributions.

        Args:
            mileage_data: Dictionary containing mileage data with 'broken' and 'functional' keys.
        """
        if not mileage_data or 'broken' not in mileage_data or 'functional' not in mileage_data:
            self.logger.warning("Insufficient mileage data for boxplot")
            return

        data = []
        labels = []

        if mileage_data['broken']:
            data.append(mileage_data['broken'])
            labels.append('Broken Motor')

        if mileage_data['functional']:
            data.append(mileage_data['functional'])
            labels.append('Functional')

        if data:
            plt.boxplot(data, tick_labels=labels)
            plt.ylabel('Mileage (km)')
            plt.title('Mileage Distribution: Broken vs Functional Cars')
            plt.grid(True, alpha=0.3)

    def _export_price_analysis(self, price_data: Dict, writer: pd.ExcelWriter) -> None:
        """Export price analysis to Excel worksheet.

        Args:
            price_data: Dictionary containing price analysis data.
            writer: ExcelWriter object for writing data.
        """
        if not price_data:
            self.logger.warning("No price data to export")
            return

        # Create summary statistics
        summary_data = {
            'Metric': ['Average', 'Median', 'Min', 'Max', 'Std Dev'],
            'Broken Motor': [
                price_data.get('broken_avg', 0),
                price_data.get('broken_median', 0),
                price_data.get('broken_min', 0),
                price_data.get('broken_max', 0),
                price_data.get('broken_std', 0)
            ],
            'Functional': [
                price_data.get('functional_avg', 0),
                price_data.get('functional_median', 0),
                price_data.get('functional_min', 0),
                price_data.get('functional_max', 0),
                price_data.get('functional_std', 0)
            ]
        }

        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name='Price Analysis', index=False)

    def _export_model_statistics(self, model_data: Dict, writer: pd.ExcelWriter) -> None:
        """Export model statistics to Excel worksheet.

        Args:
            model_data: Dictionary containing model statistics.
            writer: ExcelWriter object for writing data.
        """
        if not model_data:
            self.logger.warning("No model statistics to export")
            return

        rows = []
        for model, stats in model_data.items():
            rows.append({
                'Model': model,
                'Broken Count': stats.get('broken_count', 0),
                'Functional Count': stats.get('functional_count', 0),
                'Broken Avg Price': stats.get('broken_avg_price', 0),
                'Functional Avg Price': stats.get('functional_avg_price', 0),
                'Price Difference': stats.get('price_diff', 0)
            })

        if rows:
            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name='Model Statistics', index=False)

    def _export_mileage_analysis(self, mileage_data: Dict, writer: pd.ExcelWriter) -> None:
        """Export mileage analysis to Excel worksheet.

        Args:
            mileage_data: Dictionary containing mileage analysis data.
            writer: ExcelWriter object for writing data.
        """
        if not mileage_data:
            self.logger.warning("No mileage data to export")
            return

        summary_data = {
            'Metric': ['Average', 'Median', 'Min', 'Max', 'Std Dev'],
            'Broken Motor': [
                mileage_data.get('broken_avg', 0),
                mileage_data.get('broken_median', 0),
                mileage_data.get('broken_min', 0),
                mileage_data.get('broken_max', 0),
                mileage_data.get('broken_std', 0)
            ],
            'Functional': [
                mileage_data.get('functional_avg', 0),
                mileage_data.get('functional_median', 0),
                mileage_data.get('functional_min', 0),
                mileage_data.get('functional_max', 0),
                mileage_data.get('functional_std', 0)
            ]
        }

        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name='Mileage Analysis', index=False)

    def _export_age_analysis(self, age_data: Dict, writer: pd.ExcelWriter) -> None:
        """Export age analysis to Excel worksheet.

        Args:
            age_data: Dictionary containing age distribution data.
            writer: ExcelWriter object for writing data.
        """
        if not age_data:
            self.logger.warning("No age data to export")
            return

        summary_data = {
            'Metric': ['Average', 'Median', 'Min', 'Max', 'Std Dev'],
            'Broken Motor': [
                age_data.get('broken_avg', 0),
                age_data.get('broken_median', 0),
                age_data.get('broken_min', 0),
                age_data.get('broken_max', 0),
                age_data.get('broken_std', 0)
            ],
            'Functional': [
                age_data.get('functional_avg', 0),
                age_data.get('functional_median', 0),
                age_data.get('functional_min', 0),
                age_data.get('functional_max', 0),
                age_data.get('functional_std', 0)
            ]
        }

        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name='Age Analysis', index=False)

    def _export_summary(self, summary_data: Dict, writer: pd.ExcelWriter) -> None:
        """Export summary statistics to Excel worksheet.

        Args:
            summary_data: Dictionary containing summary statistics.
            writer: ExcelWriter object for writing data.
        """
        if not summary_data:
            self.logger.warning("No summary data to export")
            return

        rows = []
        for key, value in summary_data.items():
            rows.append({'Metric': key, 'Value': value})

        if rows:
            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name='Summary', index=False)
