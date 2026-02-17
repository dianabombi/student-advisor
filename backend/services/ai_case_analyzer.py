"""
AI Case Analyzer Service

Analyzes legal cases using RAG and provides recommendations with MANDATORY legal citations.
Every response MUST include references to specific laws, paragraphs, and articles.

Integrates with RAG system to extract citations from real Slovak laws.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re
import os
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from services.rag import create_rag_chain


class LegalCitation:
    """Represents a legal citation with law, paragraph, and article."""
    
    def __init__(self, law_name: str, paragraph: str, article: str = None, text: str = None):
        self.law_name = law_name
        self.paragraph = paragraph
        self.article = article
        self.text = text
    
    def format(self) -> str:
        """Format citation for display."""
        citation = f"**{self.law_name}**"
        if self.paragraph:
            citation += f", § {self.paragraph}"
        if self.article:
            citation += f", čl. {self.article}"
        return citation
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "law_name": self.law_name,
            "paragraph": self.paragraph,
            "article": self.article,
            "text": self.text,
            "formatted": self.format()
        }


class AICaseAnalyzer:
    """
    AI-powered case analyzer using RAG.
    
    CRITICAL: All responses MUST include legal citations from real laws.
    Uses RAG to retrieve relevant legal context from Slovak law database.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
        # Initialize RAG chain with legal-specific prompt
        self.rag_chain = create_rag_chain(
            db=db,
            model="gpt-4",
            system_prompt=self._get_legal_system_prompt()
        )
        
        # Prompt template with MANDATORY citation requirement
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Slovak legal AI assistant specializing in civil law.

CRITICAL RULES:
1. ALWAYS cite specific laws with paragraph numbers (§)
2. ALWAYS include article numbers (čl.) when applicable
3. Format citations as: **Občiansky zákonník**, § 420, čl. 1
4. Never give advice without legal citations
5. If unsure, say so and cite the closest relevant law

Available laws:
- Občiansky zákonník (Civil Code)
- Zákonník práce (Labor Code)
- Obchodný zákonník (Commercial Code)

Response format:
1. Analysis with citations
2. Recommendations with legal basis
3. Required documents
4. Confidence level (0-100%)"""),
            ("user", "{question}")
        ])
    
    def extract_citations(self, text: str) -> List[LegalCitation]:
        """
        Extract legal citations from text.
        
        Patterns:
        - § 420
        - čl. 1
        - Občiansky zákonník § 420
        """
        citations = []
        
        # Pattern: Law name, § paragraph, čl. article
        pattern = r'(\*\*[^*]+\*\*)[,\s]*§\s*(\d+)(?:[,\s]*čl\.\s*(\d+))?'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            law_name = match.group(1).strip('*')
            paragraph = match.group(2)
            article = match.group(3) if match.group(3) else None
            
            citations.append(LegalCitation(
                law_name=law_name,
                paragraph=paragraph,
                article=article
            ))
        
        return citations
    
    def _get_legal_system_prompt(self) -> str:
        """Get legal-specific system prompt for RAG."""
        return """You are a Slovak legal AI assistant specializing in Slovak law.

CRITICAL RULES:
1. ALWAYS cite specific laws with paragraph numbers (§)
2. ALWAYS include article numbers (čl.) when applicable  
3. Format citations as: **Občiansky zákonník**, § 420, čl. 1
4. Use ONLY the legal context provided below from the database
5. Never invent citations - only use what's in the context
6. If no relevant law found, say so clearly

You will receive legal context from Slovak law database.
Base your answer ONLY on this context."""
    
    async def analyze_case(self, case_data: Dict) -> Dict:
        """
        Analyze case and provide recommendations with legal citations.
        
        Args:
            case_data: Dictionary with case information
                - title: str
                - description: str
                - claim_amount: float (optional)
                - client_info: dict (optional)
        
        Returns:
            Dictionary with analysis, citations, and recommendations
        """
        # Build analysis query
        query = self._build_analysis_query(case_data)
        
        # Get RAG response with legal context from database
        rag_result = await self.rag_chain.query(
            question=query,
            filters={'practice_area': 'civil'},  # Filter by practice area
            top_k=5,
            include_sources=True
        )
        
        rag_response = rag_result['answer']
        sources = rag_result.get('sources', [])
        
        # Extract citations
        citations = self.extract_citations(rag_response)
        
        # Validate that citations exist
        if not citations:
            # Force citation by querying specific laws
            rag_response = self._force_citation(query, rag_response)
            citations = self.extract_citations(rag_response)
        
        # Determine if lawyer is needed
        needs_lawyer, confidence = self._assess_complexity(case_data, rag_response)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(case_data, rag_response, citations)
        
        # Generate required documents list
        required_docs = self._get_required_documents(case_data, citations)
        
        return {
            "analysis": rag_response,
            "citations": [c.to_dict() for c in citations],
            "needs_lawyer": needs_lawyer,
            "confidence": confidence,
            "recommendations": recommendations,
            "required_documents": required_docs,
            "suggested_status": "submitted" if confidence > 0.8 else "needs_review",
            "analyzed_at": datetime.utcnow().isoformat()
        }
    
    def _build_analysis_query(self, case_data: Dict) -> str:
        """Build query for RAG system."""
        query = f"""Analyze this legal case and provide specific legal citations:

Title: {case_data.get('title', 'N/A')}
Description: {case_data.get('description', 'N/A')}
"""
        
        if case_data.get('claim_amount'):
            query += f"\nClaim Amount: {case_data['claim_amount']} EUR"
        
        query += "\n\nProvide:\n1. Relevant laws with § and čl. numbers\n2. Legal basis for the claim\n3. Required documents\n4. Recommended actions"
        
        return query
    
    async def _force_citation(self, query: str, response: str) -> str:
        """Force AI to provide citations if none found."""
        follow_up = f"""Your previous response lacked specific legal citations.

Original query: {query}

Please provide the EXACT same analysis but with:
- Specific law names (e.g., **Občiansky zákonník**)
- Paragraph numbers (§ 420)
- Article numbers where applicable (čl. 1)

Format: **Law Name**, § paragraph, čl. article

Use ONLY the legal context from the database."""
        
        # Use RAG again with stricter prompt
        result = await self.rag_chain.query(
            question=follow_up,
            filters={'practice_area': 'civil'},
            top_k=5
        )
        return result['answer']
    
    def _assess_complexity(self, case_data: Dict, analysis: str) -> Tuple[bool, float]:
        """
        Assess if case needs human lawyer.
        
        Returns: (needs_lawyer, confidence)
        """
        # High complexity triggers
        claim_amount = case_data.get('claim_amount', 0)
        
        needs_lawyer = False
        confidence = 0.9  # Default high confidence
        
        # Trigger 1: High claim amount
        if claim_amount > 10000:
            needs_lawyer = True
            confidence = 0.6
        
        # Trigger 2: Complex legal terms in analysis
        complex_terms = ['precedent', 'constitutional', 'appeal', 'criminal']
        if any(term in analysis.lower() for term in complex_terms):
            needs_lawyer = True
            confidence = 0.5
        
        # Trigger 3: Multiple conflicting laws
        citations = self.extract_citations(analysis)
        if len(citations) > 5:
            confidence = 0.7
        
        return needs_lawyer, confidence
    
    def _generate_recommendations(self, case_data: Dict, analysis: str, citations: List[LegalCitation]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Always include legal basis
        if citations:
            legal_basis = ", ".join([c.format() for c in citations[:3]])
            recommendations.append(f"Legal basis: {legal_basis}")
        
        # Add specific recommendations based on case type
        if "debt" in case_data.get('title', '').lower() or "dlh" in case_data.get('description', '').lower():
            recommendations.extend([
                "Prepare demand letter with 15-day payment deadline",
                "Gather proof of debt (contract, invoices, bank statements)",
                "Calculate interest according to § 517 Občiansky zákonník"
            ])
        
        if "damage" in case_data.get('title', '').lower() or "škoda" in case_data.get('description', '').lower():
            recommendations.extend([
                "Document all damages with photos and expert assessment",
                "Obtain repair cost estimates",
                "File claim within 3 years (§ 101 Občiansky zákonník)"
            ])
        
        return recommendations
    
    def _get_required_documents(self, case_data: Dict, citations: List[LegalCitation]) -> List[Dict]:
        """Get list of required documents based on case type."""
        docs = [
            {
                "name": "Pozovná žaloba (Lawsuit petition)",
                "required": True,
                "can_generate": True,
                "description": "Main legal document initiating the case"
            },
            {
                "name": "Doklad totožnosti (ID document)",
                "required": True,
                "can_generate": False,
                "description": "Copy of valid ID card or passport"
            }
        ]
        
        # Add case-specific documents
        if case_data.get('claim_amount'):
            docs.append({
                "name": "Dôkaz o nároku (Proof of claim)",
                "required": True,
                "can_generate": False,
                "description": "Contract, invoice, or other proof"
            })
        
        return docs
    
    async def generate_legal_document(self, case_data: Dict, document_type: str = "lawsuit") -> Dict:
        """
        Generate legal document with citations.
        
        Args:
            case_data: Case information
            document_type: Type of document (lawsuit, demand_letter, etc.)
        
        Returns:
            Dictionary with document content and citations
        """
        # Analyze case first to get citations
        analysis = self.analyze_case(case_data)
        
        # Build document generation prompt
        prompt = f"""Generate a {document_type} in Slovak language for this case:

Title: {case_data.get('title')}
Description: {case_data.get('description')}
Claim Amount: {case_data.get('claim_amount', 'N/A')} EUR
Client: {case_data.get('client_name', 'N/A')}

Legal basis: {', '.join([c['formatted'] for c in analysis['citations']])}

Requirements:
1. Use formal Slovak legal language
2. Include ALL legal citations from analysis
3. Structure: Header, Facts, Legal Basis, Petition, Signature
4. Reference specific paragraphs and articles
5. Professional formatting

Generate complete document:"""
        
        document_content = self.llm.invoke(prompt).content
        
        return {
            "document_type": document_type,
            "content": document_content,
            "citations": analysis['citations'],
            "generated_at": datetime.utcnow().isoformat(),
            "language": "sk"
        }
    
    async def chat_with_citations(self, message: str, case_context: Dict = None) -> Dict:
        """
        Chat with AI assistant, always including legal citations.
        
        Args:
            message: User's question
            case_context: Optional case context for better responses
        
        Returns:
            Response with answer and citations
        """
        # Build context-aware query
        if case_context:
            query = f"""Case context:
Title: {case_context.get('title', 'N/A')}
Description: {case_context.get('description', 'N/A')}

User question: {message}

Provide answer with specific legal citations (law name, §, čl.)"""
        else:
            query = f"{message}\n\nProvide answer with specific legal citations (law name, §, čl.)"
        
        # Get RAG response with legal context
        rag_result = await self.rag_chain.query(
            question=query,
            filters={'practice_area': 'civil'},
            top_k=3,
            include_sources=True
        )
        response = rag_result['answer']
        
        # Extract citations
        citations = self.extract_citations(response)
        
        # Force citation if none found
        if not citations:
            response = self._force_citation(query, response)
            citations = self.extract_citations(response)
        
        return {
            "answer": response,
            "citations": [c.to_dict() for c in citations],
            "has_citations": len(citations) > 0,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global instance removed - create analyzer per-request with DB session
# Example: analyzer = AICaseAnalyzer(db)
# ai_analyzer = AICaseAnalyzer()
