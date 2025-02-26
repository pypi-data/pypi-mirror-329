# pubmed_meta_analyzer/__init__.py

# Version of the package
__version__ = "0.1"

# Import key functions/classes to make them accessible at the package level
from .extract_metadata import extract_metadata
from .merge_metadata import merge_metadata
from .find_articles import find_articles

# Optional: Define what gets imported when using `from pubmed_meta_analyzer import *`
__all__ = [
    "extract_metadata",
    "merge_metadata",
    "find_articles",
]