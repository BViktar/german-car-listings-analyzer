"""
Helper functions for the German Car Listings Analyzer.

This module provides utility functions for data cleaning, parsing,
and formatting.
"""

import re
from typing import Optional, Union


def clean_price(price_text: str) -> Optional[float]:
    """
    Extract and clean price from text.
    
    Args:
        price_text: Text containing price (e.g., "15.900 €", "€ 15900")
    
    Returns:
        Price as float or None if parsing fails
    
    Examples:
        >>> clean_price("15.900 €")
        15900.0
        >>> clean_price("€ 25,500")
        25500.0
    """
    if not price_text:
        return None
    
    # Remove currency symbols and common separators
    cleaned = re.sub(r'[€$£,.\s]', '', price_text)
    
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    
    Examples:
        >>> clean_text("  Extra   spaces  ")
        "Extra spaces"
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    cleaned = ' '.join(text.split())
    
    # Remove special characters but keep German umlauts
    # cleaned = re.sub(r'[^\w\säöüÄÖÜß\-]', '', cleaned)
    
    return cleaned.strip()


def extract_year(text: str) -> Optional[int]:
    """
    Extract year from text.
    
    Args:
        text: Text potentially containing a year
    
    Returns:
        Year as integer or None if not found
    
    Examples:
        >>> extract_year("BMW 320d, EZ 2018")
        2018
        >>> extract_year("Baujahr: 2020")
        2020
    """
    if not text:
        return None
    
    # Look for 4-digit year (1900-2099)
    pattern = r'\b(19\d{2}|20\d{2})\b'
    match = re.search(pattern, text)
    
    if match:
        return int(match.group(1))
    
    return None


def extract_mileage(text: str) -> Optional[int]:
    """
    Extract mileage from text.
    
    Args:
        text: Text containing mileage (e.g., "125.000 km", "50000km")
    
    Returns:
        Mileage as integer or None if parsing fails
    
    Examples:
        >>> extract_mileage("125.000 km")
        125000
        >>> extract_mileage("Laufleistung: 50,000 km")
        50000
    """
    if not text:
        return None
    
    # Look for numbers followed by km (with various separators)
    pattern = r'(\d{1,3}(?:[.,\s]\d{3})*)\s*km'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        # Remove separators and convert to int
        mileage_str = re.sub(r'[.,\s]', '', match.group(1))
        try:
            return int(mileage_str)
        except ValueError:
            return None
    
    return None


def format_currency(amount: Union[int, float], currency: str = '€') -> str:
    """
    Format a number as currency.
    
    Args:
        amount: Amount to format
        currency: Currency symbol (default: '€')
    
    Returns:
        Formatted currency string
    
    Examples:
        >>> format_currency(15900)
        "€15,900"
        >>> format_currency(25500.50, '$')
        "$25,500.50"
    """
    if amount is None:
        return f"{currency}0"
    
    # Format with thousand separators
    if isinstance(amount, float) and amount % 1 != 0:
        formatted = f"{amount:,.2f}"
    else:
        formatted = f"{int(amount):,}"
    
    return f"{currency}{formatted}"


def extract_make_model(title: str) -> tuple[Optional[str], Optional[str]]:
    """
    Extract car make and model from title.
    
    Args:
        title: Listing title
    
    Returns:
        Tuple of (make, model) or (None, None) if extraction fails
    
    Examples:
        >>> extract_make_model("BMW 320d Touring")
        ("BMW", "320d")
        >>> extract_make_model("Mercedes-Benz C-Klasse")
        ("Mercedes-Benz", "C-Klasse")
    """
    if not title:
        return None, None
    
    # Common German car makes
    makes = [
        'BMW', 'Mercedes-Benz', 'Mercedes', 'Audi', 'Volkswagen', 'VW',
        'Porsche', 'Opel', 'Ford', 'Renault', 'Peugeot', 'Citroën',
        'Fiat', 'Toyota', 'Honda', 'Nissan', 'Mazda', 'Skoda', 'Seat'
    ]
    
    title_upper = title.upper()
    
    for make in makes:
        if make.upper() in title_upper:
            # Found make, try to extract model
            # Split title and get the part after make
            parts = title.split()
            try:
                make_index = next(i for i, part in enumerate(parts) 
                                 if make.upper() in part.upper())
                if make_index + 1 < len(parts):
                    model = parts[make_index + 1]
                    return make, model
            except StopIteration:
                pass
            
            return make, None
    
    return None, None


def normalize_german_text(text: str) -> str:
    """
    Normalize German text for comparison.
    
    Args:
        text: German text to normalize
    
    Returns:
        Normalized text
    
    Examples:
        >>> normalize_german_text("Über")
        "uber"
    """
    if not text:
        return ""
    
    # German character replacements
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ß': 'ss'
    }
    
    normalized = text
    for german_char, replacement in replacements.items():
        normalized = normalized.replace(german_char, replacement)
    
    return normalized.lower()


def validate_listing_data(listing: dict) -> bool:
    """
    Validate that a listing has required fields.
    
    Args:
        listing: Listing dictionary to validate
    
    Returns:
        True if listing has required fields, False otherwise
    """
    required_fields = ['title', 'price']
    
    return all(field in listing and listing[field] is not None 
              for field in required_fields)
