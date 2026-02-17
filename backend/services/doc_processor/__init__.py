"""
Document Processor Module

Comprehensive document processing service for Student Advisor platform.
"""

from .storage import MinIOStorage
from .ocr_engine import OCREngine
from .classifier import DocumentClassifier
from .field_extractor import FieldExtractor
from .template_filler import TemplateFiller
from .processor import DocumentProcessor
from .ocr_service import perform_ocr, perform_ocr_batch, get_ocr_info
from .ocr_optimizer import OCROptimizer
from .document_types import (
    DocumentType,
    FieldType,
    FieldDefinition,
    get_document_fields,
    get_required_fields,
    get_document_type_info
)
from .classification_model import (
    DocumentClassificationModel,
    classify_document
)
from .field_extractor import extract_fields as extract_document_fields
from .template_filler import (
    fill_template as fill_document_template,
    generate_document as generate_filled_document
)

__all__ = [
    'MinIOStorage',
    'OCREngine',
    'DocumentClassifier',
    'FieldExtractor',
    'TemplateFiller',
    'DocumentProcessor',
    'perform_ocr',
    'perform_ocr_batch',
    'get_ocr_info',
    'OCROptimizer',
    'DocumentType',
    'FieldType',
    'FieldDefinition',
    'get_document_fields',
    'get_required_fields',
    'get_document_type_info',
    'DocumentClassificationModel',
    'classify_document',
    'extract_document_fields',
    'fill_document_template',
    'generate_filled_document'
]
