"""Tests for the CarDataVisualizer class."""

import sys
from pathlib import Path

import pytest
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.visualization import CarDataVisualizer  # noqa: E402


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_analysis_data():
    """Create sample analysis data for testing."""
    return {
        'price_comparison': {
            'broken': [5000, 6000, 5500, 7000, 6500],
            'functional': [15000, 16000, 15500, 17000, 16500],
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
                'Model A': {
                    'broken_avg': 5500,
                    'functional_avg': 15500
                },
                'Model B': {
                    'broken_avg': 6500,
                    'functional_avg': 16500
                }
            }
        },
        'age_distribution': {
            'broken': [5, 6, 7, 8, 9],
            'functional': [2, 3, 4, 5, 6],
            'broken_avg': 7.0,
            'functional_avg': 4.0,
            'broken_median': 7.0,
            'functional_median': 4.0,
            'broken_min': 5,
            'functional_min': 2,
            'broken_max': 9,
            'functional_max': 6,
            'broken_std': 1.58,
            'functional_std': 1.58
        },
        'mileage_analysis': {
            'broken': [100000, 120000, 110000, 130000, 115000],
            'functional': [50000, 60000, 55000, 65000, 58000],
            'broken_avg': 115000,
            'functional_avg': 57600,
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
            'Model A': {
                'broken_count': 3,
                'functional_count': 5,
                'broken_avg_price': 5500,
                'functional_avg_price': 15500,
                'price_diff': 10000
            },
            'Model B': {
                'broken_count': 2,
                'functional_count': 4,
                'broken_avg_price': 6500,
                'functional_avg_price': 16500,
                'price_diff': 10000
            }
        },
        'summary': {
            'total_broken': 5,
            'total_functional': 9,
            'avg_price_diff': 10000,
            'avg_age_diff': 3.0,
            'avg_mileage_diff': 57400
        }
    }


class TestCarDataVisualizer:
    """Test cases for CarDataVisualizer class."""

    def test_init_creates_output_directory(self, temp_output_dir):
        """Test that initialization creates the output directory."""
        output_path = Path(temp_output_dir) / 'test_output'
        visualizer = CarDataVisualizer(output_dir=str(output_path))

        assert output_path.exists()
        assert visualizer.output_dir == output_path

    def test_init_with_existing_directory(self, temp_output_dir):
        """Test initialization with an existing directory."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        assert Path(temp_output_dir).exists()
        assert visualizer.output_dir == Path(temp_output_dir)

    def test_create_price_comparison(self, temp_output_dir, sample_analysis_data):
        """Test price comparison visualization creation."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)
        visualizer.create_price_comparison(sample_analysis_data)

        # Check that files were created
        assert (Path(temp_output_dir) / 'price_distribution.png').exists()
        assert (Path(temp_output_dir) / 'model_price_comparison.png').exists()

    def test_create_age_distribution(self, temp_output_dir, sample_analysis_data):
        """Test age distribution visualization creation."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)
        visualizer.create_age_distribution(sample_analysis_data)

        # Check that file was created
        assert (Path(temp_output_dir) / 'age_distribution.png').exists()

    def test_create_mileage_comparison(self, temp_output_dir, sample_analysis_data):
        """Test mileage comparison visualization creation."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)
        visualizer.create_mileage_comparison(sample_analysis_data)

        # Check that file was created
        assert (Path(temp_output_dir) / 'mileage_comparison.png').exists()

    def test_export_excel_report(self, temp_output_dir, sample_analysis_data):
        """Test Excel report export."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)
        visualizer.export_excel_report(sample_analysis_data)

        # Check that Excel file was created
        excel_path = Path(temp_output_dir) / 'car_analysis.xlsx'
        assert excel_path.exists()

        # Verify that it's a valid Excel file by reading it
        excel_file = pd.ExcelFile(excel_path)
        sheet_names = excel_file.sheet_names

        # Check for expected sheets
        assert 'Price Analysis' in sheet_names
        assert 'Model Statistics' in sheet_names
        assert 'Mileage Analysis' in sheet_names
        assert 'Age Analysis' in sheet_names
        assert 'Summary' in sheet_names

    def test_price_boxplot_with_empty_data(self, temp_output_dir):
        """Test price boxplot with empty data."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Should not raise an error
        plt.figure()
        visualizer._create_price_boxplot({'broken': [], 'functional': []})
        plt.close()

    def test_model_price_comparison_with_no_model_data(self, temp_output_dir):
        """Test model price comparison with no model data."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Should not raise an error
        plt.figure()
        visualizer._create_model_price_comparison({})
        plt.close()

    def test_age_histogram_with_empty_data(self, temp_output_dir):
        """Test age histogram with empty data."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Should not raise an error
        plt.figure()
        visualizer._create_age_histogram({'broken': [], 'functional': []})
        plt.close()

    def test_mileage_boxplot_with_empty_data(self, temp_output_dir):
        """Test mileage boxplot with empty data."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Should not raise an error
        plt.figure()
        visualizer._create_mileage_boxplot({'broken': [], 'functional': []})
        plt.close()

    def test_error_handling_in_create_price_comparison(self, temp_output_dir):
        """Test error handling in create_price_comparison."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Missing required key should raise an error
        with pytest.raises(Exception):
            visualizer.create_price_comparison({})

    def test_error_handling_in_create_age_distribution(self, temp_output_dir):
        """Test error handling in create_age_distribution."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Missing required key should raise an error
        with pytest.raises(Exception):
            visualizer.create_age_distribution({})

    def test_error_handling_in_create_mileage_comparison(self, temp_output_dir):
        """Test error handling in create_mileage_comparison."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Missing required key should raise an error
        with pytest.raises(Exception):
            visualizer.create_mileage_comparison({})

    def test_error_handling_in_export_excel_report(self, temp_output_dir):
        """Test error handling in export_excel_report."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        # Missing required keys should be handled gracefully (creates empty Excel file)
        visualizer.export_excel_report({})

        # Check that Excel file was created even with no data
        assert (Path(temp_output_dir) / 'car_analysis.xlsx').exists()

    def test_logging_configuration(self, temp_output_dir):
        """Test that logger is properly configured."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        assert visualizer.logger is not None
        assert visualizer.logger.name == 'src.utils.visualization'

    def test_excel_export_with_empty_model_statistics(self, temp_output_dir):
        """Test Excel export with empty model statistics."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        analysis_data = {
            'price_comparison': {},
            'model_statistics': {},
            'mileage_analysis': {},
            'age_distribution': {},
            'summary': {}
        }

        # Should not raise an error
        visualizer.export_excel_report(analysis_data)

        # Check that Excel file was created
        assert (Path(temp_output_dir) / 'car_analysis.xlsx').exists()

    def test_visualizations_with_partial_data(self, temp_output_dir):
        """Test visualizations with partial data (only broken or only functional)."""
        visualizer = CarDataVisualizer(output_dir=temp_output_dir)

        partial_data = {
            'price_comparison': {
                'broken': [5000, 6000],
                'functional': [],
                'by_model': {}
            }
        }

        # Should not raise an error
        visualizer.create_price_comparison(partial_data)
        assert (Path(temp_output_dir) / 'price_distribution.png').exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
