"""
Configuration management for the German Car Listings Analyzer.

This module provides configuration settings for web scraping, data analysis,
and general application behavior.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for the application."""
    
    # Base URLs for German car marketplaces
    BASE_URLS = {
        'mobile_de': 'https://www.mobile.de',
        'autoscout24': 'https://www.autoscout24.de',
    }
    
    # Scraping configuration
    SCRAPING = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'timeout': 30,
        'retry_attempts': 3,
        'delay_between_requests': 2,  # seconds
    }
    
    # Search parameters for broken motor vehicles
    BROKEN_MOTOR_KEYWORDS = [
        'motorschaden',
        'defekter motor',
        'motor defekt',
        'getriebeschaden',
        'unfallschaden',
    ]
    
    # Analysis configuration
    ANALYSIS = {
        'price_comparison_enabled': True,
        'min_sample_size': 10,
        'outlier_threshold': 3,  # standard deviations
    }
    
    # Output configuration
    OUTPUT = {
        'data_dir': 'data',
        'output_dir': 'output',
        'logs_dir': 'logs',
    }
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return getattr(cls, key, default)
    
    @classmethod
    def get_url(cls, marketplace: str) -> str:
        """Get the base URL for a specific marketplace."""
        return cls.BASE_URLS.get(marketplace, '')
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        for directory in cls.OUTPUT.values():
            os.makedirs(directory, exist_ok=True)


# Initialize configuration on import
Config.ensure_directories()
