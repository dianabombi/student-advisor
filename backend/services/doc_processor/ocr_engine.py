"""
OCR Engine

Multi-engine OCR service supporting Tesseract and PaddleOCR.
"""

import os
import logging
from typing import Optional, Literal
from PIL import Image
# import cv2  # Temporarily disabled - will add opencv-python to requirements.txt
import numpy as np

logger = logging.getLogger(__name__)


class OCREngine:
    """
    OCR engine with support for multiple backends.
    
    Supports:
    - Tesseract OCR (fast, good for clean documents)
    - PaddleOCR (better for Cyrillic, handwriting)
    - Automatic image preprocessing
    """
    
    def __init__(
        self,
        engine: Literal['tesseract', 'paddle', 'auto'] = 'auto',
        languages: Optional[list] = None
    ):
        """
        Initialize OCR engine.
        
        Args:
            engine: OCR engine to use ('tesseract', 'paddle', 'auto')
            languages: List of language codes (e.g., ['eng', 'slk', 'rus'])
        """
        self.engine = engine
        self.languages = languages or ['eng', 'slk', 'rus']
        
        # Initialize engines
        self._tesseract = None
        self._paddle = None
        
        if engine in ['tesseract', 'auto']:
            self._init_tesseract()
        
        if engine in ['paddle', 'auto']:
            self._init_paddle()
    
    def _init_tesseract(self):
        """Initialize Tesseract OCR."""
        try:
            import pytesseract
            self._tesseract = pytesseract
            logger.info("Tesseract OCR initialized")
        except ImportError:
            logger.warning("Tesseract not available")
    
    def _init_paddle(self):
        """Initialize PaddleOCR."""
        try:
            from paddleocr import PaddleOCR
            
            # Determine language
            if any(lang in ['rus', 'ukr'] for lang in self.languages):
                ocr_lang = 'cyrillic'
            else:
                ocr_lang = 'en'
            
            self._paddle = PaddleOCR(
                use_angle_cls=True,
                lang=ocr_lang,
                show_log=False
            )
            logger.info(f"PaddleOCR initialized (lang: {ocr_lang})")
        except ImportError:
            logger.warning("PaddleOCR not available")
    
    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocess image for better OCR results.
        
        TEMPORARILY DISABLED - requires opencv-python
        
        Args:
            image_path: Path to input image
            
        Returns:
            Path to preprocessed image
        """
        # Disabled until opencv-python is added to requirements.txt
        logger.warning("Image preprocessing disabled (opencv not available)")
        return image_path
        
        # # Read image
        # img = cv2.imread(image_path)
        # 
        # # Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 
        # # Denoise
        # denoised = cv2.fastNlMeansDenoising(gray, h=10)
        # 
        # # Threshold
        # _, thresh = cv2.threshold(
        #     denoised, 0, 255,
        #     cv2.THRESH_BINARY + cv2.THRESH_OTSU
        # )
        # 
        # # Save preprocessed image
        # preprocessed_path = image_path.replace('.', '_preprocessed.')
        # cv2.imwrite(preprocessed_path, thresh)
        # 
        # logger.info(f"Preprocessed image: {preprocessed_path}")
        # return preprocessed_path
    
    def extract_text_tesseract(
        self,
        image_path: str,
        preprocess: bool = True
    ) -> str:
        """
        Extract text using Tesseract.
        
        Args:
            image_path: Path to image
            preprocess: Whether to preprocess image
            
        Returns:
            Extracted text
        """
        if not self._tesseract:
            raise RuntimeError("Tesseract not available")
        
        # Preprocess if needed
        if preprocess:
            image_path = self.preprocess_image(image_path)
        
        # Build language string
        lang_str = '+'.join(self.languages)
        
        # Extract text
        image = Image.open(image_path)
        text = self._tesseract.image_to_string(
            image,
            lang=lang_str,
            config='--oem 3 --psm 6'
        )
        
        logger.info(f"Tesseract extracted {len(text)} characters")
        return text.strip()
    
    def extract_text_paddle(
        self,
        image_path: str,
        preprocess: bool = False
    ) -> str:
        """
        Extract text using PaddleOCR.
        
        Args:
            image_path: Path to image
            preprocess: Whether to preprocess image
            
        Returns:
            Extracted text
        """
        if not self._paddle:
            raise RuntimeError("PaddleOCR not available")
        
        # Preprocess if needed
        if preprocess:
            image_path = self.preprocess_image(image_path)
        
        # Perform OCR
        result = self._paddle.ocr(image_path, cls=True)
        
        # Extract text from results
        if not result or not result[0]:
            return ""
        
        text_lines = []
        for line in result[0]:
            if line and len(line) >= 2:
                text_lines.append(line[1][0])
        
        text = '\n'.join(text_lines)
        
        logger.info(f"PaddleOCR extracted {len(text)} characters")
        return text.strip()
    
    def extract_text(
        self,
        image_path: str,
        preprocess: bool = True
    ) -> str:
        """
        Extract text using best available engine.
        
        Args:
            image_path: Path to image
            preprocess: Whether to preprocess image
            
        Returns:
            Extracted text
        """
        # Try PaddleOCR first (better for Cyrillic)
        if self.engine in ['paddle', 'auto'] and self._paddle:
            try:
                return self.extract_text_paddle(image_path, preprocess)
            except Exception as e:
                logger.warning(f"PaddleOCR failed: {e}")
        
        # Fallback to Tesseract
        if self.engine in ['tesseract', 'auto'] and self._tesseract:
            try:
                return self.extract_text_tesseract(image_path, preprocess)
            except Exception as e:
                logger.error(f"Tesseract failed: {e}")
                raise
        
        raise RuntimeError("No OCR engine available")
    
    def extract_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF (with OCR if needed).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            # Try text extraction first
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
            
            # If text extraction worked, return it
            if text.strip():
                logger.info(f"Extracted text from PDF: {len(text)} chars")
                return text.strip()
        
        except Exception as e:
            logger.warning(f"Text extraction failed: {e}")
        
        # Fallback to OCR
        logger.info("Falling back to OCR for PDF")
        return self._ocr_pdf(pdf_path)
    
    def _ocr_pdf(self, pdf_path: str) -> str:
        """
        OCR a PDF file.
        
        Args:
            pdf_path: Path to PDF
            
        Returns:
            Extracted text
        """
        from pdf2image import convert_from_path
        import tempfile
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # OCR each page
        text_parts = []
        for i, image in enumerate(images):
            # Save image temporarily
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                image.save(tmp.name)
                page_text = self.extract_text(tmp.name)
                text_parts.append(page_text)
                os.unlink(tmp.name)
        
        text = '\n\n'.join(text_parts)
        logger.info(f"OCR'd PDF: {len(images)} pages, {len(text)} chars")
        return text
