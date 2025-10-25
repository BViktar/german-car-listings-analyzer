"""
Broken Motor Parser for German Car Listings.

This module provides functionality to parse and extract car listings
that have broken motors or other mechanical issues from German marketplaces.
"""

import re
from typing import Dict, List, Optional, Any
from src.config import Config


class BrokenMotorParser:
    """Parser for identifying and extracting broken motor listings."""
    
    def __init__(self, keywords: Optional[List[str]] = None):
        """
        Initialize the parser.
        
        Args:
            keywords: Optional list of keywords to identify broken motors.
                     If not provided, uses default keywords from Config.
        """
        self.keywords = keywords or Config.BROKEN_MOTOR_KEYWORDS
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns from keywords for efficient matching."""
        self.patterns = [
            re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            for keyword in self.keywords
        ]
    
    def is_broken_motor(self, text: str) -> bool:
        """
        Check if the given text indicates a broken motor.
        
        Args:
            text: Text to check (title, description, etc.)
        
        Returns:
            True if text indicates broken motor, False otherwise
        """
        if not text:
            return False
        
        return any(pattern.search(text) for pattern in self.patterns)
    
    def extract_broken_indicators(self, text: str) -> List[str]:
        """
        Extract all broken motor indicators from text.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of matched keywords indicating broken motor
        """
        if not text:
            return []
        
        matches = []
        for keyword, pattern in zip(self.keywords, self.patterns):
            if pattern.search(text):
                matches.append(keyword)
        
        return matches
    
    def parse_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a car listing and extract broken motor information.
        
        Args:
            listing_data: Dictionary containing listing information with keys like
                         'title', 'description', 'price', etc.
        
        Returns:
            Enhanced listing dictionary with broken motor analysis
        """
        result = listing_data.copy()
        
        # Combine title and description for analysis
        text_to_analyze = ' '.join([
            listing_data.get('title', ''),
            listing_data.get('description', '')
        ])
        
        # Analyze for broken motor indicators
        result['has_broken_motor'] = self.is_broken_motor(text_to_analyze)
        result['broken_indicators'] = self.extract_broken_indicators(text_to_analyze)
        
        return result
    
    def filter_broken_listings(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter a list of listings to only include those with broken motors.
        
        Args:
            listings: List of listing dictionaries
        
        Returns:
            List of listings that have broken motors
        """
        return [
            self.parse_listing(listing)
            for listing in listings
            if self.is_broken_motor(' '.join([
                listing.get('title', ''),
                listing.get('description', '')
            ]))
        ]
    
    def categorize_listings(self, listings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorize listings into broken and functional.
        
        Args:
            listings: List of listing dictionaries
        
        Returns:
            Dictionary with 'broken' and 'functional' keys containing respective listings
        """
        broken = []
        functional = []
        
        for listing in listings:
            parsed = self.parse_listing(listing)
            if parsed['has_broken_motor']:
                broken.append(parsed)
            else:
                functional.append(parsed)
        
        return {
            'broken': broken,
            'functional': functional
        }
