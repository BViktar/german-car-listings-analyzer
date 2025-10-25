"""Scraper package for German car listing websites."""
from .base_scraper import BaseScraper
from .autoscout_scraper import AutoScout24Scraper

__all__ = ['BaseScraper', 'AutoScout24Scraper']
