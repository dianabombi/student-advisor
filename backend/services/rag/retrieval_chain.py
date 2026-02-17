"""
RAG Retrieval Chain for Student Advisor Platform

Implements retrieval-augmented generation pipeline using OpenAI v1.0+ API:
1. Query embedding
2. Context retrieval via vector similarity
3. Answer generation with OpenAI ChatCompletion

Usage:
    from services.rag.retrieval_chain import RetrievalChain
    
    chain = RetrievalChain(db=db_session)
    result = await chain.query("Aké sú podmienky platnosti zmluvy?", k=3)
"""

import os
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI


class RetrievalChain:
    """
    Complete RAG retrieval chain for legal document Q&A.
    
    Features:
    - Query embedding with OpenAI
    - Vector similarity search (L2 distance)
    - Context retrieval from document chunks
    - Answer generation with OpenAI ChatCompletion
    - Customizable prompts
    """
    
    def __init__(
        self,
        db: Session,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.0
    ):
        """
        Initialize retrieval chain.
        
        Args:
            db: SQLAlchemy database session
            api_key: OpenAI API key (defaults to env variable)
            model: OpenAI model for generation
            temperature: Model temperature (0 = deterministic)
        """
        self.db = db
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        
        # Initialize OpenAI client (v1.0+ syntax)
        self.client = OpenAI(api_key=self.api_key)
        
        # Default system prompt
        self.system_prompt = self._default_system_prompt()
    
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
   Príklad: "Na Slovensku Občiansky zákonník upravuje zmluvy v §§ 34-51..."
   
✅ Ukazovať relevantné články zákonov
   Príklad: "Podľa § 97 Zákonníka práce, práca cez víkend sa kompenzuje..."
   
✅ Poskytovať šablóny dokumentov s disclaimerom
   Príklad: "Tu je vzorová sťažnosť. ⚠️ Odporúčam overenie právnikom."
   
✅ Vysvetľovať právne procedúry
   Príklad: "Proces podania sťažnosti: 1) Napísať sťažnosť, 2) Podať na súd..."
   
✅ Analyzovať dokumenty s disclaimerom
   Príklad: "V tejto zmluve vidím tieto riziká... ⚠️ Toto je všeobecná analýza, nie právna rada."

❌ ČO NESMIEŠ ROBIŤ (Red Zone):
❌ Konkrétne právne rady pre prípad používateľa
   ZLYHANIE: "VY by ste mali podať žalobu"
   SPRÁVNE: "Všeobecne, pri porušení zmluvy možno podať žalobu. Odporúčam konzultáciu s advokátom."

❌ Interpretácia zákona pre konkrétnu situáciu
   ZLYHANIE: "Tento zákon znamená, že VY máte nárok na €500"
   SPRÁVNE: "Podľa tohto zákona môže vzniknúť nárok na kompenzáciu. Pre posúdenie VÁŠHO prípadu kontaktujte advokáta."

❌ Garancie výsledkov
   ZLYHANIE: "Určite vyhráte súd"
   SPRÁVNE: "Výsledok závisí od mnohých faktorov. Advokát posúdi vaše šance."

❌ Zastupovanie
   ZLYHANIE: "Napíšem pozov za vás"
   SPRÁVNE: "Môžem ukázať vzor pozvu. Odporúčam, aby ho pripravil advokát."

⚠️ POVINNÉ PRAVIDLÁ:
1. VŽDY začni odpoveď disclaimerom: "🤖 Student Advisor je vzdelávacia platforma a neposkytuje profesionálne poradenstvo. Táto informácia je určená len na všeobecné vzdelávacie účely."
2. NIKDY nepoužívaj "VY by ste mali", "VÁŠ prípad", "určite vyhráte"
3. VŽDY odporúčaj konzultáciu s advokátom pre konkrétne situácie
4. Používaj "všeobecne", "zvyčajne", "môže", nie "musíte", "určite"

Odpovedaj v slovenčine, jasne a profesionálne."""

    
    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using OpenAI (v1.0+ syntax).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Embedding error: {e}")
            raise
    
    async def retrieve_context(
        self,
        query: str,
        k: int = 3,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Retrieve relevant document chunks for query.
        
        Args:
            query: User's question
            k: Number of documents to retrieve
            filters: Optional filters (practice_area, jurisdiction, etc.)
            
        Returns:
            List of document chunks with metadata
        """
        # Step 1: Generate query embedding
        query_embedding = self._get_embedding(query)
        
        # Step 2: Build SQL query with filters
        filter_conditions = []
        params = {
            'query_embedding': query_embedding,
            'k': k
        }
        
        if filters:
            if 'practice_area' in filters:
                filter_conditions.append("d.practice_area = :practice_area")
                params['practice_area'] = filters['practice_area']
            
            if 'jurisdiction' in filters:
                filter_conditions.append("d.jurisdiction = :jurisdiction")
                params['jurisdiction'] = filters['jurisdiction']
            
            if 'document_type' in filters:
                filter_conditions.append("d.document_type = :document_type")
                params['document_type'] = filters['document_type']
        
        where_clause = ""
        if filter_conditions:
            where_clause = "WHERE " + " AND ".join(filter_conditions)
        
        # Step 3: Execute vector similarity search (L2 distance)
        query_sql = text(f"""
            SELECT 
                dc.id as chunk_id,
                dc.document_id,
                dc.chunk_index,
                dc.content,
                dc.chunk_metadata,
                d.filename,
                d.document_type,
                d.practice_area,
                d.jurisdiction,
                dc.embedding <-> :query_embedding as distance
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            {where_clause}
            ORDER BY dc.embedding <-> :query_embedding
            LIMIT :k
        """)
        
        results = self.db.execute(query_sql, params).fetchall()
        
        # Step 4: Format results
        chunks = []
        for row in results:
            chunks.append({
                'chunk_id': row[0],
                'document_id': row[1],
                'chunk_index': row[2],
                'content': row[3],
                'metadata': row[4],
                'filename': row[5],
                'document_type': row[6],
                'practice_area': row[7],
                'jurisdiction': row[8],
                'distance': float(row[9])
            })
        
        return chunks
    
    def _format_context(self, chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into context string.
        
        Args:
            chunks: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "Žiadne relevantné dokumenty neboli nájdené."
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            filename = chunk.get('filename', 'Neznámy dokument')
            content = chunk.get('content', '')
            
            context_parts.append(f"[Dokument {i}: {filename}]\n{content}\n")
        
        return "\n".join(context_parts)
    
    async def generate_answer(
        self,
        query: str,
        context_chunks: List[Dict]
    ) -> Dict:
        """
        Generate answer using retrieved context and OpenAI (v1.0+ syntax).
        
        Args:
            query: User's question
            context_chunks: Retrieved document chunks
            
        Returns:
            Dictionary with answer and metadata
        """
        # Format context
        context_text = self._format_context(context_chunks)
        
        # Build messages
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context_text and context_text != "Žiadne relevantné dokumenty neboli nájdené.":
            messages.append({
                "role": "system",
                "content": f"Kontext z právnych dokumentov:\n\n{context_text}"
            })
        
        messages.append({"role": "user", "content": query})
        
        # Generate answer using v1.0+ syntax
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            answer = response.choices[0].message.content
            
            # Inject UPL disclaimer at the beginning
            try:
                from services.upl_compliance import inject_disclaimer, detect_language
                language = detect_language(query)
                answer = inject_disclaimer(answer, language)
            except ImportError:
                # Fallback: prepend Slovak disclaimer if module not available
                disclaimer = "⚠️ Student Advisor je vzdelávacia platforma a neposkytuje profesionálne poradenstvo. Táto informácia je určená len na všeobecné vzdelávacie účely."
                if disclaimer not in answer:
                    answer = f"{disclaimer}\n\n{answer}"
                    
        except Exception as e:
            print(f"Error generating answer: {e}")
            answer = "Prepáčte, vyskytla sa chyba pri generovaní odpovede. Skúste to prosím znova."
        
        return {
            'answer': answer,
            'sources': [
                {
                    'filename': chunk.get('filename'),
                    'chunk_index': chunk.get('chunk_index'),
                    'distance': chunk.get('distance')
                }
                for chunk in context_chunks
            ],
            'context': context_text
        }
    
    async def query(
        self,
        question: str,
        k: int = 3,
        filters: Optional[Dict] = None,
        include_context: bool = False
    ) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate answer.
        
        Args:
            question: User's question
            k: Number of chunks to retrieve
            filters: Optional filters for retrieval
            include_context: Whether to include raw context in response
            
        Returns:
            Dictionary with answer, sources, and optionally context
        """
        # Step 1: Retrieve context
        chunks = await self.retrieve_context(query=question, k=k, filters=filters)
        
        # Step 2: Generate answer
        result = await self.generate_answer(query=question, context_chunks=chunks)
        
        # Step 3: Format response
        response = {
            'answer': result['answer'],
            'sources': result['sources']
        }
        
        if include_context:
            response['context'] = result['context']
        
        return response


# Convenience functions for backward compatibility

async def retrieve_context(
    query: str,
    k: int = 3,
    db: Session = None,
    filters: Optional[Dict] = None
) -> List[Dict]:
    """
    Retrieve relevant context for query.
    
    Args:
        query: User's question
        k: Number of chunks to retrieve
        db: Database session
        filters: Optional filters
        
    Returns:
        List of document chunks
    """
    if db is None:
        raise ValueError("Database session required")
    
    chain = RetrievalChain(db=db)
    return await chain.retrieve_context(query=query, k=k, filters=filters)


async def generate_answer(
    query: str,
    context_text: str,
    db: Session = None
) -> str:
    """
    Generate answer from query and context.
    
    Args:
        query: User's question
        context_text: Context string or list of chunks
        db: Database session
        
    Returns:
        Generated answer
    """
    if db is None:
        raise ValueError("Database session required")
    
    chain = RetrievalChain(db=db)
    
    # Handle both string context and chunk list
    if isinstance(context_text, str):
        # Create dummy chunks from string
        chunks = [{'content': context_text, 'filename': 'Context', 'chunk_index': 0, 'distance': 0.0}]
    else:
        chunks = context_text
    
    result = await chain.generate_answer(query=query, context_chunks=chunks)
    return result['answer']
