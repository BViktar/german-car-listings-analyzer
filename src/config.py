"""Configuration settings for German Car Listings Analyzer."""

import os
from pathlib import Path
from typing import Dict, Any

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"

# Create output directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Website URLs and endpoints
AUTOSCOUT24_BASE_URL = "https://www.autoscout24.de"
AUTOSCOUT24_SEARCH_URL = f"{AUTOSCOUT24_BASE_URL}/lst"

MOBILE_DE_BASE_URL = "https://www.mobile.de"
MOBILE_DE_SEARCH_URL = f"{MOBILE_DE_BASE_URL}/auto-inserate"

# Scraping configuration
SCRAPING_CONFIG: Dict[str, Any] = {
    # Delay between requests (in seconds)
    "request_delay_min": 2,
    "request_delay_max": 5,
    
    # Timeout settings
    "page_load_timeout": 30,
    "element_wait_timeout": 10,
    
    # Retry settings
    "max_retries": 3,
    "retry_delay": 5,
    
    # Batch settings
    "batch_size": 50,
    "max_pages": 10,
    
    # User agent rotation
    "rotate_user_agent": True,
    
    # Browser settings
    "headless": True,
    "browser_type": "chromium",  # chromium, firefox, or webkit
}

# Logging configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(OUTPUT_DIR / "scraper.log"),
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Output file paths
OUTPUT_FILES: Dict[str, Path] = {
    "broken_motors_csv": OUTPUT_DIR / "broken_motors.csv",
    "functional_motors_csv": OUTPUT_DIR / "functional_motors.csv",
    "comparison_csv": OUTPUT_DIR / "comparison_analysis.csv",
    "summary_excel": OUTPUT_DIR / "analysis_summary.xlsx",
    "price_chart": OUTPUT_DIR / "price_comparison.png",
}

# Search parameters
SEARCH_PARAMS: Dict[str, Any] = {
    # Common search filters
    "default_filters": {
        "make": None,  # e.g., "BMW", "Mercedes-Benz"
        "model": None,  # e.g., "3 Series", "C-Class"
        "year_min": 2010,
        "year_max": 2024,
        "mileage_max": 200000,
    },
    
    # Broken motor filters
    "broken_motor_keywords": [
        "Motorschaden",
        "defekter Motor",
        "Motor defekt",
        "Getriebeschaden",
    ],
}

# Data extraction fields
EXTRACTION_FIELDS = [
    "title",
    "price",
    "year",
    "mileage",
    "fuel_type",
    "transmission",
    "horsepower",
    "location",
    "seller_type",
    "description",
    "url",
    "condition",
    "listing_date",
]

# Environment variables
PROXY_URL = os.getenv("PROXY_URL", None)
USE_PROXY = os.getenv("USE_PROXY", "false").lower() == "true"
