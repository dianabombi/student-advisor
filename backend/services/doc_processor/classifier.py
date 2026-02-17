"""
Document Classifier

Reuses the existing classifier from services/document_classifier.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from document_classifier import DocumentClassifier as BaseClassifier

# Re-export
DocumentClassifier = BaseClassifier
