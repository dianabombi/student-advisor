"""
RAG Chain for Student Advisor Platform

Combines retrieval and generation for context-aware AI responses.
Integrates with LangChain for flexible prompt engineering.
"""

from typing import List, Dict, Optional
import openai
from .embeddings import EmbeddingService
from .retriever import DocumentRetriever


class RAGChain:
    """
    Complete RAG pipeline: Query → Retrieve → Generate.
    
    Features:
    - Automatic query embedding
    - Context retrieval from documents
    - Prompt construction with retrieved context
    - AI response generation
    - Source attribution
    """
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        retriever: DocumentRetriever,
        model: str = "gpt-4",
        system_prompt: Optional[str] = None
    ):
        """
        Initialize RAG chain.
        
        Args:
            embedding_service: Service for generating embeddings
            retriever: Service for retrieving relevant chunks
            model: OpenAI model for generation
            system_prompt: Custom system prompt (optional)
        """
        self.embedding_service = embedding_service
        self.retriever = retriever
        self.model = model
        self.system_prompt = system_prompt or self._default_system_prompt()
    
    def _default_system_prompt(self) -> str:
        """Get default UPL-compliant system prompt for legal consultation."""
        # Import UPL compliance module
        try:
            from services.upl_compliance import get_system_prompt
            return get_system_prompt(language='sk')
        except ImportError:
            # Fallback to inline UPL-compliant prompt if module not available
            return """Si asistent pre právne informácie (NIE právnik) špecializujúci sa na slovenské právo.

🔵 ČO MÔŽEŠ ROBIŤ (Safe Zone):
✅ Vysvetľovať všeobecné právne princípy
✅ Ukazovať relevantné články zákonov
✅ Poskytovať šablóny dokumentov s disclaimerom
✅ Vysvetľovať právne procedúry
✅ Analyzovať dokumenty s disclaimerom

❌ ČO NESMIEŠ ROBIŤ (Red Zone):
❌ Konkrétne právne rady pre prípad používateľa
❌ Interpretácia zákona pre konkrétnu situáciu
❌ Garancie výsledkov
❌ Zastupovanie

⚠️ POVINNÉ PRAVIDLÁ:
1. VŽDY začni odpoveď disclaimerom
2. NIKDY nepoužívaj "VY by ste mali", "VÁŠ prípad"
3. VŽDY odporúčaj konzultáciu s advokátom
4. Používaj "všeobecne", "zvyčajne", "môže"

Odpovedaj v slovenčine, jasne a profesionálne."""

    
    async def query(
        self,
        question: str,
        filters: Optional[Dict] = None,
        top_k: int = 5,
        include_sources: bool = True
    ) -> Dict:
        """
        Execute complete RAG pipeline.
        
        Args:
            question: User's question
            filters: Optional filters for retrieval
            top_k: Number of chunks to retrieve
            include_sources: Whether to include source attribution
            
        Returns:
            Dictionary with 'answer' and optionally 'sources'
        """
        # Step 1: Generate query embedding
        query_embedding = await self.embedding_service.embed_text(question)
        
        # Step 2: Retrieve relevant chunks
        chunks = await self.retriever.retrieve(
            query_embedding=query_embedding,
            filters=filters,
            top_k=top_k
        )
        
        # Step 3: Build context from retrieved chunks
        context = self._build_context(chunks)
        
        # Step 4: Generate AI response
        answer = await self._generate_response(question, context)
        
        # Step 5: Format result
        result = {'answer': answer}
        
        if include_sources and chunks:
            result['sources'] = self._format_sources(chunks)
        
        return result
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """
        Build context string from retrieved chunks.
        
        Args:
            chunks: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return ""
        
        context_parts = ["Relevantné časti z vašich dokumentov:\n"]
        
        for chunk in chunks:
            filename = chunk.get('filename', 'Unknown')
            content = chunk.get('content', '')
            similarity = chunk.get('similarity', 0)
            
            context_parts.append(
                f"\n[{filename}] (Relevancia: {similarity*100:.0f}%)\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    async def _generate_response(self, question: str, context: str) -> str:
        """
        Generate AI response using OpenAI.
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            AI-generated answer
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": question})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # Inject UPL disclaimer
            try:
                from services.upl_compliance import inject_disclaimer, detect_language
                language = detect_language(question)
                answer = inject_disclaimer(answer, language)
            except ImportError:
                # Fallback disclaimer
                disclaimer = "⚠️ Student Advisor je vzdelávacia platforma a neposkytuje profesionálne poradenstvo. Táto informácia je určená len na všeobecné vzdelávacie účely."
                if disclaimer not in answer:
                    answer = f"{disclaimer}\n\n{answer}"
            
            return answer
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Prepáčte, momentálne nemôžem spracovať vašu otázku. Skúste to prosím neskôr."
    
    def _format_sources(self, chunks: List[Dict]) -> List[Dict]:
        """
        Format source attribution for response.
        
        Args:
            chunks: Retrieved chunks
            
        Returns:
            List of formatted source references
        """
        sources = []
        for chunk in chunks:
            sources.append({
                'document_id': chunk.get('document_id'),
                'filename': chunk.get('filename'),
                'chunk_index': chunk.get('chunk_index'),
                'content': chunk.get('content', '')[:200] + '...',  # Truncate for display
                'similarity': chunk.get('similarity', 0)
            })
        return sources
    
    def set_system_prompt(self, prompt: str):
        """Update the system prompt."""
        self.system_prompt = prompt
    
    def set_model(self, model: str):
        """Update the OpenAI model."""
        self.model = model
