""" 
IndianConstitution: A Python module for accessing and managing Constitution data.
This module provides functionality to retrieve articles, search keywords, 
list articles, and much more from a JSON file containing Constitution data.
"""

import os
from .indianconstitution import IndianConstitution

__title__ = 'IndianConstitution'
__version__ = '0.5.9'
__author__ = 'Vikhram S'
__license__ = 'Apache License 2.0'

# Exported symbols for top-level import
__all__ = [
    'IndianConstitution',
    'get_preamble',
    'get_article',
    'list_articles',
    'search_keyword',
    'get_article_summary',
    'count_total_articles',
    'search_by_title',
]

# Automatically locate the default JSON file in the package directory
def _get_default_json_path():
    """Locate the default JSON file included in the package."""
    package_dir = os.path.dirname(__file__)
    return os.path.join(package_dir, 'constitution_of_india.json')

# Functions for easier direct usage
def get_preamble() -> str:
    """Retrieve the Preamble of the Constitution."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.preamble()

def get_article(number: str) -> str:
    """
    Retrieve the details of a specific article.
    Supports both numeric (e.g., 41) and alphanumeric (e.g., 41A) article numbers.
    """
    # Ensure the input is properly formatted
    if not isinstance(number, (int, str)):
        raise ValueError("Article number must be an integer or string.")

    # Convert integer to string for consistency
    number_str = str(number)

    # Instance of the IndianConstitution library
    instance = IndianConstitution(_get_default_json_path())

    # Fetch and return the article details
    return instance.get_article(number_str)
    
def list_articles() -> str:
    """List all articles in the Constitution."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.articles_list()

def search_keyword(keyword: str) -> str:
    """Search for a keyword in the Constitution."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.search_keyword(keyword)

def get_article_summary(number: int) -> str:
    """Provide a brief summary of the specified article."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.article_summary(number)

def count_total_articles() -> int:
    """Count the total number of articles in the Constitution."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.count_articles()

def search_by_title(title_keyword: str) -> str:
    """Search for articles by title keyword."""
    instance = IndianConstitution(_get_default_json_path())
    return instance.search_by_title(title_keyword)
