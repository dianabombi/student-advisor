"""
Document Classification Model

Hybrid classification using rule-based and ML approaches.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import Counter
import numpy as np

from .document_types import DocumentType

logger = logging.getLogger(__name__)


class DocumentClassificationModel:
    """
    Hybrid document classification model.
    
    Features:
    - Rule-based classification (keyword matching)
    - TF-IDF scoring
    - Optional transformer support (BERT)
    - Confidence scoring
    """
    
    # Keyword patterns for each document type
    CLASSIFICATION_RULES = {
        DocumentType.EMPLOYMENT_CONTRACT: {
            'keywords': [
                'pracovná zmluva', 'employment contract', 'zamestnanec', 'zamestnávateľ',
                'pracovný pomer', 'mzda', 'plat', 'pracovná pozícia', 'pracovisko'
            ],
            'weight': 1.0
        },
        DocumentType.PURCHASE_AGREEMENT: {
            'keywords': [
                'kúpna zmluva', 'purchase agreement', 'predávajúci', 'kupujúci',
                'kúpna cena', 'predaj', 'kúpa', 'nadobúdateľ'
            ],
            'weight': 1.0
        },
        DocumentType.LEASE_AGREEMENT: {
            'keywords': [
                'nájomná zmluva', 'lease agreement', 'prenajímateľ', 'nájomca',
                'nájomné', 'prenájom', 'nájom', 'nehnuteľnosť'
            ],
            'weight': 1.0
        },
        DocumentType.SERVICE_CONTRACT: {
            'keywords': [
                'zmluva o poskytovaní služieb', 'service contract', 'poskytovateľ služieb',
                'objednávateľ', 'služby', 'poskytovanie služieb'
            ],
            'weight': 1.0
        },
        DocumentType.WORK_CONTRACT: {
            'keywords': [
                'zmluva o dielo', 'work contract', 'zhotoviteľ', 'objednávateľ diela',
                'dielo', 'zhotovenie', 'odovzdanie diela'
            ],
            'weight': 1.0
        },
        DocumentType.INVOICE: {
            'keywords': [
                'faktúra', 'invoice', 'dodávateľ', 'odberateľ', 'suma k úhrade',
                'dátum splatnosti', 'variabilný symbol', 'IČO', 'DIČ', 'DPH'
            ],
            'weight': 1.2
        },
        DocumentType.POWER_OF_ATTORNEY: {
            'keywords': [
                'plná moc', 'power of attorney', 'splnomocniteľ', 'splnomocnenec',
                'splnomocnenie', 'zastupovanie', 'konať v mene'
            ],
            'weight': 1.0
        },
        DocumentType.COURT_DECISION: {
            'keywords': [
                'rozsudok', 'uznesenie', 'court decision', 'súd', 'žalobca', 'žalovaný',
                'spisová značka', 'rozhodnutie súdu', 'v mene republiky'
            ],
            'weight': 1.1
        },
        DocumentType.LAWSUIT: {
            'keywords': [
                'žaloba', 'lawsuit', 'žalobca', 'žalovaný', 'žalobný návrh',
                'návrh na začatie konania', 'súdny spor'
            ],
            'weight': 1.0
        },
        DocumentType.ACT: {
            'keywords': [
                'protokol', 'act', 'zápis', 'odovzdávací protokol', 'preberací protokol',
                'kontrolný záznam', 'účastníci', 'prítomní'
            ],
            'weight': 0.9
        },
        DocumentType.LETTER: {
            'keywords': [
                'list', 'letter', 'vážený', 'vážená', 's pozdravom', 'korešpondencia',
                'oznam', 'oznámenie'
            ],
            'weight': 0.8
        },
        DocumentType.APPLICATION: {
            'keywords': [
                'žiadosť', 'application', 'žiadam', 'prosím', 'podanie',
                'návrh na', 'žiadateľ'
            ],
            'weight': 0.9
        },
        DocumentType.COMPLAINT: {
            'keywords': [
                'sťažnosť', 'complaint', 'sťažujem sa', 'reklamácia',
                'nesúhlas', 'podnet'
            ],
            'weight': 1.0
        },
        DocumentType.CERTIFICATE: {
            'keywords': [
                'osvedčenie', 'certificate', 'potvrdenie', 'certifikát',
                'osvedčuje sa', 'potvrdzuje sa'
            ],
            'weight': 0.9
        },
    }
    
    def __init__(self, use_transformers: bool = False):
        """
        Initialize classification model.
        
        Args:
            use_transformers: Use transformer model (BERT) if available
        """
        self.use_transformers = use_transformers
        self.transformer_model = None
        
        if use_transformers:
            self._init_transformer()
    
    def _init_transformer(self):
        """Initialize transformer model (optional)."""
        try:
            from transformers import pipeline
            
            self.transformer_model = pipeline(
                'text-classification',
                model='bert-base-multilingual-cased',
                device=-1  # CPU
            )
            logger.info("Transformer model loaded")
        except ImportError:
            logger.warning("Transformers not available, using rule-based only")
            self.use_transformers = False
        except Exception as e:
            logger.error(f"Error loading transformer: {e}")
            self.use_transformers = False
    
    def classify_document(
        self,
        text: str,
        return_all_scores: bool = False
    ) -> Dict:
        """
        Classify document and return type with confidence.
        
        Args:
            text: Document text
            return_all_scores: Return scores for all document types
            
        Returns:
            Dictionary with document_type, confidence, and optionally all_scores
        """
        logger.info(f"Classifying document ({len(text)} chars)")
        
        # Normalize text
        text_lower = text.lower()
        
        # Calculate scores for each document type
        scores = {}
        
        for doc_type, rules in self.CLASSIFICATION_RULES.items():
            score = self._calculate_rule_score(text_lower, rules)
            scores[doc_type] = score
        
        # Get best match
        if not scores:
            return {
                'document_type': DocumentType.OTHER,
                'confidence': 0.0,
                'method': 'default'
            }
        
        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]
        
        # Normalize confidence (0-1)
        max_possible_score = max(
            len(rules['keywords']) * rules['weight']
            for rules in self.CLASSIFICATION_RULES.values()
        )
        confidence = min(best_score / max_possible_score, 1.0) if max_possible_score > 0 else 0.0
        
        # Boost confidence if score is significantly higher than others
        if len(scores) > 1:
            sorted_scores = sorted(scores.values(), reverse=True)
            if len(sorted_scores) > 1 and sorted_scores[0] > sorted_scores[1] * 2:
                confidence = min(confidence * 1.2, 1.0)
        
        result = {
            'document_type': best_type,
            'confidence': confidence,
            'method': 'rule_based'
        }
        
        if return_all_scores:
            # Normalize all scores
            result['all_scores'] = {
                doc_type.value: min(score / max_possible_score, 1.0)
                for doc_type, score in scores.items()
            }
        
        logger.info(f"Classification: {best_type.value} (confidence: {confidence:.2%})")
        
        return result
    
    def _calculate_rule_score(self, text: str, rules: Dict) -> float:
        """
        Calculate score based on keyword matching.
        
        Args:
            text: Normalized text (lowercase)
            rules: Classification rules
            
        Returns:
            Score
        """
        keywords = rules['keywords']
        weight = rules['weight']
        
        # Count keyword occurrences
        score = 0.0
        for keyword in keywords:
            # Count occurrences (with word boundaries)
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text))
            
            if matches > 0:
                # Score increases with matches, but with diminishing returns
                score += weight * (1 + np.log1p(matches))
        
        return score
    
    def classify_with_context(
        self,
        text: str,
        filename: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Classify document with additional context.
        
        Args:
            text: Document text
            filename: Optional filename
            metadata: Optional metadata
            
        Returns:
            Classification result
        """
        # Base classification
        result = self.classify_document(text, return_all_scores=True)
        
        # Boost confidence based on filename
        if filename:
            filename_lower = filename.lower()
            
            for doc_type in DocumentType:
                type_name = doc_type.value.replace('_', ' ')
                if type_name in filename_lower:
                    if result['document_type'] == doc_type:
                        result['confidence'] = min(result['confidence'] * 1.3, 1.0)
                        logger.info(f"Confidence boosted by filename match")
                        break
        
        # Use metadata if available
        if metadata:
            if 'document_type' in metadata:
                suggested_type = metadata['document_type']
                if suggested_type == result['document_type'].value:
                    result['confidence'] = min(result['confidence'] * 1.2, 1.0)
                    logger.info(f"Confidence boosted by metadata match")
        
        return result
    
    def batch_classify(self, texts: List[str]) -> List[Dict]:
        """
        Classify multiple documents.
        
        Args:
            texts: List of document texts
            
        Returns:
            List of classification results
        """
        logger.info(f"Batch classifying {len(texts)} documents")
        
        results = []
        for i, text in enumerate(texts):
            try:
                result = self.classify_document(text)
                results.append(result)
            except Exception as e:
                logger.error(f"Error classifying document {i}: {e}")
                results.append({
                    'document_type': DocumentType.OTHER,
                    'confidence': 0.0,
                    'error': str(e)
                })
        
        return results
    
    def get_classification_explanation(
        self,
        text: str,
        result: Dict
    ) -> Dict:
        """
        Get explanation for classification result.
        
        Args:
            text: Document text
            result: Classification result
            
        Returns:
            Explanation dictionary
        """
        text_lower = text.lower()
        doc_type = result['document_type']
        
        if doc_type not in self.CLASSIFICATION_RULES:
            return {'matched_keywords': [], 'explanation': 'No rules for this type'}
        
        rules = self.CLASSIFICATION_RULES[doc_type]
        matched_keywords = []
        
        for keyword in rules['keywords']:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text_lower)
            if matches:
                matched_keywords.append({
                    'keyword': keyword,
                    'count': len(matches)
                })
        
        return {
            'matched_keywords': matched_keywords,
            'total_matches': sum(k['count'] for k in matched_keywords),
            'explanation': f"Matched {len(matched_keywords)} keywords from {len(rules['keywords'])} total"
        }


# Convenience function
def classify_document(text: str, **kwargs) -> Dict:
    """
    Classify a document.
    
    Args:
        text: Document text
        **kwargs: Additional arguments for classifier
        
    Returns:
        Classification result
    """
    classifier = DocumentClassificationModel()
    return classifier.classify_document(text, **kwargs)
