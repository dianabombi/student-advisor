"""
Document Processor

Main orchestrator for document processing pipeline.
"""

import os
import logging
import tempfile
from typing import Dict, Optional
from pathlib import Path

from .storage import MinIOStorage
from .ocr_engine import OCREngine
from .classifier import DocumentClassifier
from .field_extractor import FieldExtractor
from .template_filler import TemplateFiller

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Complete document processing pipeline.
    
    Pipeline:
    1. Upload to MinIO
    2. Extract text (OCR if needed)
    3. Classify document
    4. Extract key fields
    5. Generate filled template (optional)
    """
    
    def __init__(
        self,
        storage: Optional[MinIOStorage] = None,
        ocr: Optional[OCREngine] = None,
        classifier: Optional[DocumentClassifier] = None,
        extractor: Optional[FieldExtractor] = None,
        filler: Optional[TemplateFiller] = None
    ):
        """
        Initialize document processor.
        
        Args:
            storage: MinIO storage service
            ocr: OCR engine
            classifier: Document classifier
            extractor: Field extractor
            filler: Template filler
        """
        self.storage = storage or MinIOStorage()
        self.ocr = ocr or OCREngine(engine='auto')
        self.classifier = classifier or DocumentClassifier()
        self.extractor = extractor or FieldExtractor()
        self.filler = filler or TemplateFiller()
    
    def process_document(
        self,
        file_data: bytes,
        filename: str,
        extract_fields: bool = True,
        use_ai: bool = True
    ) -> Dict:
        """
        Process a document through the complete pipeline.
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            extract_fields: Whether to extract fields
            use_ai: Whether to use AI for classification
            
        Returns:
            Processing results
        """
        logger.info(f"Processing document: {filename}")
        
        # 1. Upload to MinIO
        object_name = f"uploads/{filename}"
        self.storage.upload_file(file_data, object_name)
        
        # 2. Extract text
        text = self._extract_text(file_data, filename)
        
        # 3. Classify document
        classification = self.classifier.analyze_document(text, use_ai=use_ai)
        
        # 4. Extract fields (if requested)
        fields = None
        if extract_fields:
            fields = self.extractor.extract_all_fields(text)
        
        # 5. Generate summary
        summary = self.filler.generate_summary({
            'classification': classification['classification'],
            'parties': fields['parties'] if fields else [],
            'dates': fields['dates'] if fields else [],
            'amounts': fields['amounts'] if fields else [],
            'identifiers': fields['identifiers'] if fields else {}
        })
        
        result = {
            'filename': filename,
            'object_name': object_name,
            'text_length': len(text),
            'classification': classification,
            'extracted_fields': fields,
            'summary': summary,
            'storage_url': self.storage.get_presigned_url(object_name)
        }
        
        logger.info(f"Document processed: {filename}")
        return result
    
    def _extract_text(self, file_data: bytes, filename: str) -> str:
        """
        Extract text from file.
        
        Args:
            file_data: File content
            filename: Filename
            
        Returns:
            Extracted text
        """
        file_ext = Path(filename).suffix.lower()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            # Extract based on file type
            if file_ext == '.txt':
                text = file_data.decode('utf-8')
            
            elif file_ext == '.pdf':
                text = self.ocr.extract_from_pdf(tmp_path)
            
            elif file_ext == '.docx':
                from docx import Document
                doc = Document(tmp_path)
                text = '\n'.join([p.text for p in doc.paragraphs])
            
            elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff']:
                text = self.ocr.extract_text(tmp_path)
            
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            logger.info(f"Extracted {len(text)} characters from {filename}")
            return text
        
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def create_filled_template(
        self,
        template_name: str,
        extracted_data: Dict,
        output_filename: str
    ) -> str:
        """
        Create a filled template from extracted data.
        
        Args:
            template_name: Name of template
            extracted_data: Extracted data
            output_filename: Output filename
            
        Returns:
            Object name in MinIO
        """
        logger.info(f"Creating filled template: {template_name}")
        
        # Get template from MinIO
        template_object = f"templates/{template_name}"
        template_data = self.storage.download_file(template_object)
        
        # Save template temporarily
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_template:
            tmp_template.write(template_data)
            template_path = tmp_template.name
        
        # Create output path
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_output:
            output_path = tmp_output.name
        
        try:
            # Fill template
            self.filler.fill_template(template_path, extracted_data, output_path)
            
            # Upload filled document
            with open(output_path, 'rb') as f:
                filled_data = f.read()
            
            object_name = f"filled/{output_filename}"
            self.storage.upload_file(filled_data, object_name, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            
            logger.info(f"Filled template uploaded: {object_name}")
            return object_name
        
        finally:
            # Cleanup
            if os.path.exists(template_path):
                os.unlink(template_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def batch_process(self, files: list) -> list:
        """
        Process multiple documents.
        
        Args:
            files: List of (file_data, filename) tuples
            
        Returns:
            List of processing results
        """
        logger.info(f"Batch processing {len(files)} documents")
        
        results = []
        for file_data, filename in files:
            try:
                result = self.process_document(file_data, filename)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {filename}: {e}")
                results.append({
                    'filename': filename,
                    'error': str(e)
                })
        
        return results
