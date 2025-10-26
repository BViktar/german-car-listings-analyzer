"""Tests for CSV report generator."""
import csv
import os
import tempfile
from pathlib import Path
import pytest
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.csv_report import CarReportGenerator


class TestCarReportGenerator:
    """Test suite for CarReportGenerator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def sample_broken_cars(self):
        """Sample broken cars data."""
        return [
            {
                'make': 'BMW',
                'model': '320i',
                'year': 2015,
                'price': 5000,
                'url': 'https://example.com/broken1'
            },
            {
                'make': 'Audi',
                'model': 'A4',
                'year': 2016,
                'price': 6000,
                'url': 'https://example.com/broken2'
            }
        ]
    
    @pytest.fixture
    def sample_functional_cars(self):
        """Sample functional cars data."""
        return [
            {
                'make': 'BMW',
                'model': '320i',
                'year': 2015,
                'price': 12000,
                'mileage': 80000,
                'url': 'https://example.com/func1'
            },
            {
                'make': 'BMW',
                'model': '320i',
                'year': 2016,
                'price': 14000,
                'mileage': 60000,
                'url': 'https://example.com/func2'
            },
            {
                'make': 'Audi',
                'model': 'A4',
                'year': 2016,
                'price': 15000,
                'mileage': 70000,
                'url': 'https://example.com/func3'
            }
        ]
    
    def test_init_creates_output_directory(self, temp_dir):
        """Test that __init__ creates the output directory."""
        output_dir = os.path.join(temp_dir, 'test_reports')
        generator = CarReportGenerator(output_dir=output_dir)
        
        assert os.path.exists(output_dir)
        assert generator.output_dir == Path(output_dir)
    
    def test_group_by_make_model(self, temp_dir, sample_functional_cars):
        """Test grouping cars by make and model."""
        generator = CarReportGenerator(output_dir=temp_dir)
        grouped = generator._group_by_make_model(sample_functional_cars)
        
        assert 'BMW_320i' in grouped
        assert 'Audi_A4' in grouped
        assert len(grouped['BMW_320i']) == 2
        assert len(grouped['Audi_A4']) == 1
    
    def test_generate_main_report(self, temp_dir, sample_broken_cars, sample_functional_cars):
        """Test generating main broken cars report."""
        generator = CarReportGenerator(output_dir=temp_dir)
        functional_grouped = generator._group_by_make_model(sample_functional_cars)
        
        main_report_path = Path(temp_dir) / 'broken_cars_report.csv'
        generator._generate_main_report(sample_broken_cars, functional_grouped, main_report_path)
        
        assert main_report_path.exists()
        
        # Read and verify content
        with open(main_report_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        
        # Check first row (BMW)
        assert rows[0]['car_description'] == '2015 BMW 320i'
        assert rows[0]['advertisement_link'] == 'https://example.com/broken1'
        assert rows[0]['price'] == '5000'
        assert rows[0]['average_similar_price'] == '13000.0'  # (12000 + 14000) / 2
        assert rows[0]['similar_cars_file'] == 'similar_cars_BMW_320i.csv'
        
        # Check second row (Audi)
        assert rows[1]['car_description'] == '2016 Audi A4'
        assert rows[1]['advertisement_link'] == 'https://example.com/broken2'
        assert rows[1]['price'] == '6000'
        assert rows[1]['average_similar_price'] == '15000.0'
        assert rows[1]['similar_cars_file'] == 'similar_cars_Audi_A4.csv'
    
    def test_generate_similar_cars_reports(self, temp_dir, sample_functional_cars):
        """Test generating similar cars reports."""
        generator = CarReportGenerator(output_dir=temp_dir)
        functional_grouped = generator._group_by_make_model(sample_functional_cars)
        
        generator._generate_similar_cars_reports(functional_grouped)
        
        # Check BMW report
        bmw_report = Path(temp_dir) / 'similar_cars_BMW_320i.csv'
        assert bmw_report.exists()
        
        with open(bmw_report, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]['make'] == 'BMW'
        assert rows[0]['model'] == '320i'
        assert rows[0]['year'] == '2015'
        assert rows[0]['price'] == '12000'
        assert rows[0]['mileage'] == '80000'
        
        # Check Audi report
        audi_report = Path(temp_dir) / 'similar_cars_Audi_A4.csv'
        assert audi_report.exists()
        
        with open(audi_report, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]['make'] == 'Audi'
        assert rows[0]['model'] == 'A4'
    
    def test_generate_reports_full_workflow(self, temp_dir, sample_broken_cars, sample_functional_cars):
        """Test the full report generation workflow."""
        generator = CarReportGenerator(output_dir=temp_dir)
        generator.generate_reports(sample_broken_cars, sample_functional_cars)
        
        # Check that main report exists
        main_report = Path(temp_dir) / 'broken_cars_report.csv'
        assert main_report.exists()
        
        # Check that similar car reports exist
        bmw_report = Path(temp_dir) / 'similar_cars_BMW_320i.csv'
        audi_report = Path(temp_dir) / 'similar_cars_Audi_A4.csv'
        assert bmw_report.exists()
        assert audi_report.exists()
    
    def test_empty_broken_cars_list(self, temp_dir, sample_functional_cars):
        """Test handling empty broken cars list."""
        generator = CarReportGenerator(output_dir=temp_dir)
        generator.generate_reports([], sample_functional_cars)
        
        # Main report should exist but be empty (except header)
        main_report = Path(temp_dir) / 'broken_cars_report.csv'
        assert main_report.exists()
        
        with open(main_report, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 0
    
    def test_empty_functional_cars_list(self, temp_dir, sample_broken_cars):
        """Test handling empty functional cars list."""
        generator = CarReportGenerator(output_dir=temp_dir)
        generator.generate_reports(sample_broken_cars, [])
        
        # Main report should exist with zero average price
        main_report = Path(temp_dir) / 'broken_cars_report.csv'
        assert main_report.exists()
        
        with open(main_report, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]['average_similar_price'] == '0'
        assert rows[0]['similar_cars_file'] == ''
    
    def test_utf8_encoding_german_characters(self, temp_dir):
        """Test UTF-8 encoding for German characters."""
        broken_cars = [
            {
                'make': 'Volkswagen',
                'model': 'Käfer',
                'year': 2010,
                'price': 3000,
                'url': 'https://example.com/käfer'
            }
        ]
        
        functional_cars = [
            {
                'make': 'Volkswagen',
                'model': 'Käfer',
                'year': 2010,
                'price': 8000,
                'mileage': 50000,
                'url': 'https://example.com/käfer-func'
            }
        ]
        
        generator = CarReportGenerator(output_dir=temp_dir)
        generator.generate_reports(broken_cars, functional_cars)
        
        # Read and verify German characters are preserved
        main_report = Path(temp_dir) / 'broken_cars_report.csv'
        with open(main_report, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Käfer' in content
        
        similar_report = Path(temp_dir) / 'similar_cars_Volkswagen_Käfer.csv'
        assert similar_report.exists()
        with open(similar_report, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Käfer' in content
    
    def test_no_matching_functional_cars(self, temp_dir):
        """Test when broken car has no matching functional cars."""
        broken_cars = [
            {
                'make': 'Mercedes',
                'model': 'C200',
                'year': 2015,
                'price': 7000,
                'url': 'https://example.com/merc'
            }
        ]
        
        functional_cars = [
            {
                'make': 'BMW',
                'model': '320i',
                'year': 2015,
                'price': 12000,
                'mileage': 80000,
                'url': 'https://example.com/bmw'
            }
        ]
        
        generator = CarReportGenerator(output_dir=temp_dir)
        generator.generate_reports(broken_cars, functional_cars)
        
        # Check main report
        main_report = Path(temp_dir) / 'broken_cars_report.csv'
        with open(main_report, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]['average_similar_price'] == '0'
        assert rows[0]['similar_cars_file'] == ''
        
        # Mercedes similar cars file should not be created
        merc_report = Path(temp_dir) / 'similar_cars_Mercedes_C200.csv'
        assert not merc_report.exists()
