"""
AI SERVICE
AI analysis and document generation for legal cases
"""

import os
from openai import OpenAI
from typing import Dict, List
from models.client import AIAnalysisResponse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_case(case) -> AIAnalysisResponse:
    """
    Analyze legal case using AI
    
    Returns:
    - Complexity score (1-10)
    - Success probability (0-100%)
    - Recommended action
    - Estimated time and cost
    - Required documents
    - Options (self-service, document review, full service)
    """
    
    # Prepare prompt for AI
    prompt = f"""
You are a legal AI assistant analyzing a case for a Slovak client.

CASE DETAILS:
Title: {case.title}
Description: {case.description}
Category: {case.category}
Type: {case.case_type}
Urgency: {case.urgency}

TASK:
Analyze this case and provide:
1. Complexity score (1-10, where 10 is most complex)
2. Success probability (0-100%)
3. Recommended action
4. Estimated time to resolve
5. Estimated cost range
6. Key points to consider
7. Required documents
8. Available options (self-service, document review, full legal service)

Respond in JSON format.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal AI assistant specializing in Slovak law."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse AI response (simplified - would use structured output)
        ai_text = response.choices[0].message.content
        
        # Mock structured response for now
        analysis = AIAnalysisResponse(
            complexity_score=_estimate_complexity(case),
            success_probability=_estimate_success_probability(case),
            recommended_action=_get_recommended_action(case),
            estimated_time=_estimate_time(case),
            estimated_cost_range=_estimate_cost(case),
            key_points=_extract_key_points(case),
            required_documents=_get_required_documents(case),
            options=_get_service_options(case)
        )
        
        return analysis
        
    except Exception as e:
        # Fallback to rule-based analysis
        return AIAnalysisResponse(
            complexity_score=5,
            success_probability=70.0,
            recommended_action="Odporúčame konzultáciu s advokátom",
            estimated_time="1-2 týždne",
            estimated_cost_range={"min": 100, "max": 500, "currency": "EUR"},
            key_points=[
                "Potrebné zhromaždiť dôkazy",
                "Dodržať lehoty",
                "Konzultovať s odborníkom"
            ],
            required_documents=[
                "Doklad o zaplatení",
                "Fotokópia lístka",
                "Písomná sťažnosť"
            ],
            options=[
                {
                    "type": "self_service",
                    "name": "Vlastné riešenie",
                    "price": 0,
                    "description": "AI vygeneruje dokument, ktorý môžete použiť sami"
                },
                {
                    "type": "document_review",
                    "name": "Kontrola dokumentu",
                    "price": 150,
                    "description": "Advokát skontroluje váš dokument"
                },
                {
                    "type": "full_service",
                    "name": "Plná právna služba",
                    "price": 500,
                    "description": "Advokát sa postará o celý prípad"
                }
            ]
        )


async def generate_document(case) -> Dict:
    """
    Generate legal document using AI
    """
    
    prompt = f"""
Generate a legal document for this case:

Title: {case.title}
Description: {case.description}
Category: {case.category}
Type: {case.case_type}

Generate a professional legal document in Slovak language.
Include all necessary legal formalities.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal document generator for Slovak law."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        document_text = response.choices[0].message.content
        
        return {
            "content": document_text,
            "preview": document_text[:500] + "...",
            "format": "text"
        }
        
    except Exception as e:
        return {
            "content": "Error generating document",
            "preview": "Error",
            "format": "text"
        }


# Helper functions for rule-based analysis

def _estimate_complexity(case) -> int:
    """Estimate case complexity (1-10)"""
    complexity_map = {
        "transport_law": 3,
        "consumer_protection": 4,
        "labor_law": 6,
        "family_law": 7,
        "real_estate": 8,
        "criminal_law": 9,
        "civil_law": 5
    }
    return complexity_map.get(case.category, 5)


def _estimate_success_probability(case) -> float:
    """Estimate success probability (0-100%)"""
    # Simple rule-based estimation
    base_probability = 70.0
    
    if case.urgency == "urgent":
        base_probability -= 10
    
    if len(case.description) > 500:
        base_probability += 5  # More details = better case
    
    return min(max(base_probability, 0), 100)


def _get_recommended_action(case) -> str:
    """Get recommended action"""
    complexity = _estimate_complexity(case)
    
    if complexity <= 3:
        return "Môžete to vyriešiť sami s pomocou AI generovaného dokumentu"
    elif complexity <= 6:
        return "Odporúčame konzultáciu s advokátom alebo kontrolu dokumentu"
    else:
        return "Odporúčame plnú právnu službu advokáta"


def _estimate_time(case) -> str:
    """Estimate time to resolve"""
    complexity = _estimate_complexity(case)
    
    if complexity <= 3:
        return "1-2 týždne"
    elif complexity <= 6:
        return "2-4 týždne"
    else:
        return "1-3 mesiace"


def _estimate_cost(case) -> Dict:
    """Estimate cost range"""
    complexity = _estimate_complexity(case)
    
    cost_ranges = {
        1: {"min": 0, "max": 100},
        2: {"min": 50, "max": 150},
        3: {"min": 100, "max": 250},
        4: {"min": 150, "max": 350},
        5: {"min": 200, "max": 500},
        6: {"min": 300, "max": 700},
        7: {"min": 500, "max": 1000},
        8: {"min": 700, "max": 1500},
        9: {"min": 1000, "max": 3000},
        10: {"min": 2000, "max": 5000}
    }
    
    cost_range = cost_ranges.get(complexity, {"min": 200, "max": 500})
    cost_range["currency"] = "EUR"
    
    return cost_range


def _extract_key_points(case) -> List[str]:
    """Extract key points from case"""
    return [
        "Zhromaždite všetky relevantné dokumenty",
        "Dodržte zákonné lehoty",
        "Zdokumentujte všetku komunikáciu",
        "Zvážte mediáciu pred súdnym sporom"
    ]


def _get_required_documents(case) -> List[str]:
    """Get required documents for case type"""
    doc_map = {
        "transport_law": [
            "Lístok alebo doklad o zaplatení",
            "Fotografie/dôkazy",
            "Písomná sťažnosť",
            "Korešpondencia s dopravcom"
        ],
        "consumer_protection": [
            "Kúpna zmluva",
            "Faktúra",
            "Reklamačný protokol",
            "Fotografie vady"
        ],
        "labor_law": [
            "Pracovná zmluva",
            "Výpoveď",
            "Mzdové lístky",
            "Korešpondencia so zamestnávateľom"
        ]
    }
    
    return doc_map.get(case.category, [
        "Všetky relevantné zmluvy",
        "Dôkazy a dokumenty",
        "Korešpondencia"
    ])


def _get_service_options(case) -> List[Dict]:
    """Get available service options"""
    complexity = _estimate_complexity(case)
    cost_range = _estimate_cost(case)
    
    options = [
        {
            "type": "self_service",
            "name": "Vlastné riešenie s AI",
            "price": 0,
            "description": "AI vygeneruje dokument, ktorý môžete použiť sami",
            "recommended": complexity <= 3
        },
        {
            "type": "document_review",
            "name": "Kontrola dokumentu advokátom",
            "price": cost_range["min"],
            "description": "Advokát skontroluje a upraví váš dokument",
            "recommended": 3 < complexity <= 6
        },
        {
            "type": "full_service",
            "name": "Plná právna služba",
            "price": cost_range["max"],
            "description": "Advokát sa postará o celý prípad od začiatku do konca",
            "recommended": complexity > 6
        }
    ]
    
    return options
