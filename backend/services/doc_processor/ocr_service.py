"""
Unified OCR Service

Main OCR function for the Student Advisor platform.
"""

import os
import logging
from typing import List, Dict, Optional, Union
from pathlib import Path
import tempfile

from .ocr_engine import OCREngine

logger = logging.getLogger(__name__)


def perform_ocr(
    file_path: str,
    languages: Optional[List[str]] = None,
    engine: str = 'auto',
    return_pages: bool = False,
    preprocess: bool = True
) -> Union[str, List[Dict]]:
    """
    Perform OCR on PDF or image file.
    
    This is the main OCR function for the Student Advisor platform.
    Supports PDF, images (JPG, PNG, TIFF), and multi-page documents.
    
    Args:
        file_path: Path to PDF or image file
        languages: List of language codes (default: ['eng', 'slk', 'rus'])
        engine: OCR engine ('tesseract', 'paddle', 'auto')
        return_pages: If True, return list of pages with metadata
        preprocess: Whether to preprocess images
        
    Returns:
        If return_pages=False: Concatenated text from all pages
        If return_pages=True: List of dicts with page number, text, and confidence
        
    Examples:
        >>> # Simple OCR
        >>> text = perform_ocr('document.pdf')
        >>> print(text)
        
        >>> # OCR with page information
        >>> pages = perform_ocr('document.pdf', return_pages=True)
        >>> for page in pages:
        >>>     print(f"Page {page['page_number']}: {page['text'][:100]}...")
        
        >>> # OCR with specific languages
        >>> text = perform_ocr('document.pdf', languages=['slk', 'ces'])
    """
    logger.info(f"Performing OCR on: {file_path}")
    
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Initialize OCR engine
    ocr = OCREngine(
        engine=engine,
        languages=languages or ['eng', 'slk', 'rus']
    )
    
    # Determine file type
    file_ext = Path(file_path).suffix.lower()
    
    # Process based on file type
    if file_ext == '.pdf':
        result = _ocr_pdf(file_path, ocr, return_pages, preprocess)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        result = _ocr_image(file_path, ocr, return_pages, preprocess)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    logger.info(f"OCR completed: {file_path}")
    return result


def _ocr_pdf(
    pdf_path: str,
    ocr: OCREngine,
    return_pages: bool,
    preprocess: bool
) -> Union[str, List[Dict]]:
    """
    OCR a PDF file.
    
    Args:
        pdf_path: Path to PDF
        ocr: OCR engine instance
        return_pages: Return page-by-page results
        preprocess: Preprocess images
        
    Returns:
        Text or list of page results
    """
    from pdf2image import convert_from_path
    
    logger.info(f"Converting PDF to images: {pdf_path}")
    
    # Convert PDF to images
    try:
        images = convert_from_path(pdf_path, dpi=300)
    except Exception as e:
        logger.error(f"Error converting PDF: {e}")
        # Fallback: try text extraction first
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
            
            if text.strip():
                logger.info("Used text extraction instead of OCR")
                if return_pages:
                    return [{'page_number': i+1, 'text': page.extract_text(), 'method': 'text_extraction'} 
                            for i, page in enumerate(pdf_reader.pages)]
                return text
        except:
            pass
        raise
    
    logger.info(f"Processing {len(images)} pages")
    
    # OCR each page
    pages_data = []
    all_text = []
    
    for i, image in enumerate(images):
        page_num = i + 1
        logger.info(f"OCR page {page_num}/{len(images)}")
        
        # Save image temporarily
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name, 'PNG')
            tmp_path = tmp.name
        
        try:
            # Perform OCR
            page_text = ocr.extract_text(tmp_path, preprocess=preprocess)
            
            all_text.append(page_text)
            
            if return_pages:
                pages_data.append({
                    'page_number': page_num,
                    'text': page_text,
                    'char_count': len(page_text),
                    'method': 'ocr'
                })
        
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    if return_pages:
        return pages_data
    else:
        return '\n\n'.join(all_text)


def _ocr_image(
    image_path: str,
    ocr: OCREngine,
    return_pages: bool,
    preprocess: bool
) -> Union[str, List[Dict]]:
    """
    OCR an image file.
    
    Args:
        image_path: Path to image
        ocr: OCR engine instance
        return_pages: Return as page result
        preprocess: Preprocess image
        
    Returns:
        Text or list with single page result
    """
    logger.info(f"OCR image: {image_path}")
    
    # Perform OCR
    text = ocr.extract_text(image_path, preprocess=preprocess)
    
    if return_pages:
        return [{
            'page_number': 1,
            'text': text,
            'char_count': len(text),
            'method': 'ocr'
        }]
    else:
        return text


def perform_ocr_batch(
    file_paths: List[str],
    **kwargs
) -> List[Dict]:
    """
    Perform OCR on multiple files.
    
    Args:
        file_paths: List of file paths
        **kwargs: Arguments passed to perform_ocr
        
    Returns:
        List of results with filename and text/pages
    """
    logger.info(f"Batch OCR: {len(file_paths)} files")
    
    results = []
    for file_path in file_paths:
        try:
            result = perform_ocr(file_path, **kwargs)
            results.append({
                'filename': os.path.basename(file_path),
                'filepath': file_path,
                'result': result,
                'success': True
            })
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            results.append({
                'filename': os.path.basename(file_path),
                'filepath': file_path,
                'error': str(e),
                'success': False
            })
    
    return results


def get_ocr_info() -> Dict:
    """
    Get information about available OCR engines.
    
    Returns:
        Dictionary with OCR engine information
    """
    info = {
        'tesseract': False,
        'paddle': False,
        'tesseract_languages': [],
        'paddle_languages': ['en', 'latin', 'cyrillic']
    }
    
    # Check Tesseract
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        info['tesseract'] = True
        info['tesseract_version'] = str(version)
        
        # Get available languages
        langs = pytesseract.get_languages()
        info['tesseract_languages'] = langs
    except:
        pass
    
    # Check PaddleOCR
    try:
        from paddleocr import PaddleOCR
        info['paddle'] = True
    except:
        pass
    
    return info


# Convenience functions
def ocr_pdf(pdf_path: str, **kwargs) -> str:
    """OCR a PDF file and return concatenated text."""
    return perform_ocr(pdf_path, **kwargs)


def ocr_image(image_path: str, **kwargs) -> str:
    """OCR an image file and return text."""
    return perform_ocr(image_path, **kwargs)


def ocr_pdf_pages(pdf_path: str, **kwargs) -> List[Dict]:
    """OCR a PDF file and return page-by-page results."""
    return perform_ocr(pdf_path, return_pages=True, **kwargs)
