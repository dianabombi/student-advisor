"""
OCR Optimization Module

Advanced image preprocessing and OCR validation.

TEMPORARILY DISABLED - requires opencv-python
"""

# import cv2  # Temporarily disabled - will add opencv-python to requirements.txt
import numpy as np
import logging
from typing import Tuple, Dict, Optional
from PIL import Image
import tempfile
import os

logger = logging.getLogger(__name__)


class OCROptimizer:
    """
    OCR optimization with advanced image preprocessing.
    
    Features:
    - Auto-rotation detection and correction
    - Binarization (Otsu, adaptive)
    - Contrast enhancement
    - Noise removal
    - Deskewing
    - Quality validation
    """
    
    def __init__(self):
        """Initialize OCR optimizer."""
        self.min_text_length = 50  # Minimum characters for valid OCR
        self.min_confidence = 0.5  # Minimum confidence score
    
    def preprocess_image(
        self,
        image_path: str,
        auto_rotate: bool = True,
        enhance_contrast: bool = True,
        denoise: bool = True,
        binarize: bool = True,
        deskew: bool = True
    ) -> str:
        """
        Comprehensive image preprocessing for OCR.
        
        Args:
            image_path: Path to input image
            auto_rotate: Auto-detect and fix rotation
            enhance_contrast: Enhance image contrast
            denoise: Remove noise
            binarize: Convert to binary (black/white)
            deskew: Fix skewed text
            
        Returns:
            Path to preprocessed image
        """
        logger.info(f"Preprocessing image: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Auto-rotate if needed
        if auto_rotate:
            gray = self._auto_rotate(gray)
        
        # Deskew
        if deskew:
            gray = self._deskew(gray)
        
        # Denoise
        if denoise:
            gray = self._denoise(gray)
        
        # Enhance contrast
        if enhance_contrast:
            gray = self._enhance_contrast(gray)
        
        # Binarize
        if binarize:
            gray = self._binarize(gray)
        
        # Save preprocessed image
        output_path = image_path.replace('.', '_optimized.')
        cv2.imwrite(output_path, gray)
        
        logger.info(f"Preprocessed image saved: {output_path}")
        return output_path
    
    def _auto_rotate(self, image: np.ndarray) -> np.ndarray:
        """
        Auto-detect and correct image rotation.
        
        Args:
            image: Input image
            
        Returns:
            Rotated image
        """
        # Detect text orientation using edge detection
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is None:
            return image
        
        # Calculate dominant angle
        angles = []
        for line in lines[:20]:  # Use top 20 lines
            rho, theta = line[0]
            angle = np.degrees(theta) - 90
            angles.append(angle)
        
        if not angles:
            return image
        
        # Get median angle
        median_angle = np.median(angles)
        
        # Only rotate if angle is significant
        if abs(median_angle) > 0.5:
            logger.info(f"Auto-rotating by {median_angle:.2f} degrees")
            
            # Rotate image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            return rotated
        
        return image
    
    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Fix skewed text.
        
        Args:
            image: Input image
            
        Returns:
            Deskewed image
        """
        # Calculate skew angle
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image
        
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Only deskew if angle is significant
        if abs(angle) > 0.5:
            logger.info(f"Deskewing by {angle:.2f} degrees")
            
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            deskewed = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            return deskewed
        
        return image
    
    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Remove noise from image.
        
        Args:
            image: Input image
            
        Returns:
            Denoised image
        """
        # Use Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoising(image, h=10)
        logger.info("Applied denoising")
        return denoised
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image contrast using CLAHE.
        
        Args:
            image: Input image
            
        Returns:
            Contrast-enhanced image
        """
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        logger.info("Enhanced contrast with CLAHE")
        return enhanced
    
    def _binarize(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image to binary (black and white).
        
        Args:
            image: Input image
            
        Returns:
            Binary image
        """
        # Otsu's binarization
        _, binary = cv2.threshold(
            image, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        logger.info("Applied Otsu binarization")
        return binary
    
    def validate_ocr_result(
        self,
        text: str,
        image_path: Optional[str] = None
    ) -> Dict:
        """
        Validate OCR result quality.
        
        Args:
            text: OCR result text
            image_path: Optional path to source image
            
        Returns:
            Validation result with quality metrics
        """
        logger.info("Validating OCR result")
        
        # Calculate metrics
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.split('\n'))
        
        # Check for valid characters (not just noise)
        alphanumeric_count = sum(c.isalnum() for c in text)
        alphanumeric_ratio = alphanumeric_count / char_count if char_count > 0 else 0
        
        # Determine quality
        is_valid = True
        issues = []
        
        # Check minimum text length
        if char_count < self.min_text_length:
            is_valid = False
            issues.append(f"Too little text extracted ({char_count} chars, min {self.min_text_length})")
        
        # Check alphanumeric ratio
        if alphanumeric_ratio < 0.5:
            is_valid = False
            issues.append(f"Low alphanumeric ratio ({alphanumeric_ratio:.2%})")
        
        # Check for excessive special characters (noise)
        special_char_ratio = sum(not c.isalnum() and not c.isspace() for c in text) / char_count if char_count > 0 else 0
        if special_char_ratio > 0.3:
            is_valid = False
            issues.append(f"Too many special characters ({special_char_ratio:.2%})")
        
        # Calculate confidence score
        confidence = min(
            alphanumeric_ratio,
            1.0 - special_char_ratio,
            min(char_count / self.min_text_length, 1.0)
        )
        
        result = {
            'is_valid': is_valid,
            'confidence': confidence,
            'char_count': char_count,
            'word_count': word_count,
            'line_count': line_count,
            'alphanumeric_ratio': alphanumeric_ratio,
            'special_char_ratio': special_char_ratio,
            'issues': issues,
            'needs_retry': not is_valid and confidence < 0.3
        }
        
        if is_valid:
            logger.info(f"OCR validation passed (confidence: {confidence:.2%})")
        else:
            logger.warning(f"OCR validation failed: {', '.join(issues)}")
        
        return result
    
    def optimize_and_validate(
        self,
        image_path: str,
        ocr_function,
        max_retries: int = 3
    ) -> Dict:
        """
        Optimize image and validate OCR with automatic retry.
        
        Args:
            image_path: Path to image
            ocr_function: OCR function to call
            max_retries: Maximum retry attempts
            
        Returns:
            Dictionary with text, validation, and metadata
        """
        logger.info(f"Starting optimized OCR with validation: {image_path}")
        
        attempts = []
        
        # Try 1: Original image
        logger.info("Attempt 1: Original image")
        text = ocr_function(image_path)
        validation = self.validate_ocr_result(text, image_path)
        
        attempts.append({
            'attempt': 1,
            'method': 'original',
            'text': text,
            'validation': validation
        })
        
        if validation['is_valid']:
            logger.info("OCR successful on first attempt")
            return {
                'text': text,
                'validation': validation,
                'attempts': 1,
                'method': 'original'
            }
        
        # Try 2: Basic preprocessing
        if max_retries >= 2:
            logger.info("Attempt 2: Basic preprocessing")
            preprocessed = self.preprocess_image(
                image_path,
                auto_rotate=False,
                enhance_contrast=True,
                denoise=True,
                binarize=True,
                deskew=False
            )
            
            try:
                text = ocr_function(preprocessed)
                validation = self.validate_ocr_result(text)
                
                attempts.append({
                    'attempt': 2,
                    'method': 'basic_preprocessing',
                    'text': text,
                    'validation': validation
                })
                
                if validation['is_valid']:
                    logger.info("OCR successful with basic preprocessing")
                    return {
                        'text': text,
                        'validation': validation,
                        'attempts': 2,
                        'method': 'basic_preprocessing'
                    }
            finally:
                if os.path.exists(preprocessed):
                    os.unlink(preprocessed)
        
        # Try 3: Full preprocessing
        if max_retries >= 3:
            logger.info("Attempt 3: Full preprocessing")
            preprocessed = self.preprocess_image(
                image_path,
                auto_rotate=True,
                enhance_contrast=True,
                denoise=True,
                binarize=True,
                deskew=True
            )
            
            try:
                text = ocr_function(preprocessed)
                validation = self.validate_ocr_result(text)
                
                attempts.append({
                    'attempt': 3,
                    'method': 'full_preprocessing',
                    'text': text,
                    'validation': validation
                })
                
                if validation['is_valid']:
                    logger.info("OCR successful with full preprocessing")
                    return {
                        'text': text,
                        'validation': validation,
                        'attempts': 3,
                        'method': 'full_preprocessing'
                    }
            finally:
                if os.path.exists(preprocessed):
                    os.unlink(preprocessed)
        
        # Return best attempt
        best_attempt = max(attempts, key=lambda x: x['validation']['confidence'])
        logger.warning(f"OCR completed with low confidence after {len(attempts)} attempts")
        
        return {
            'text': best_attempt['text'],
            'validation': best_attempt['validation'],
            'attempts': len(attempts),
            'method': best_attempt['method'],
            'all_attempts': attempts
        }
