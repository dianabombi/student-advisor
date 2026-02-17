"""
UPL Compliance Tests for CODEX Legal Platform

Tests to ensure AI responses comply with Unauthorized Practice of Law regulations.
"""

import pytest
from services.upl_compliance import (
    UPLCompliance,
    get_disclaimer,
    get_system_prompt,
    inject_disclaimer,
    validate_compliance
)


class TestDisclaimers:
    """Test multilingual disclaimer functionality."""
    
    def test_slovak_disclaimer(self):
        """Test Slovak disclaimer contains required elements."""
        disclaimer = get_disclaimer('sk')
        assert "⚠️" in disclaimer
        assert "CODEX nie je právnická firma" in disclaimer
        assert "neposkytuje právne poradenstvo" in disclaimer
        assert "licencovaného advokáta" in disclaimer
    
    def test_english_disclaimer(self):
        """Test English disclaimer contains required elements."""
        disclaimer = get_disclaimer('en')
        assert "⚠️" in disclaimer
        assert "CODEX is not a law firm" in disclaimer
        assert "does not provide legal advice" in disclaimer
        assert "licensed attorney" in disclaimer
    
    def test_all_languages_have_disclaimers(self):
        """Test all 10 languages have disclaimers."""
        languages = ['sk', 'en', 'uk', 'ru', 'de', 'it', 'fr', 'es', 'pl', 'cs']
        for lang in languages:
            disclaimer = get_disclaimer(lang)
            assert len(disclaimer) > 50, f"Disclaimer for {lang} is too short"
            assert "⚠️" in disclaimer, f"Disclaimer for {lang} missing warning emoji"
            assert "CODEX" in disclaimer, f"Disclaimer for {lang} missing CODEX mention"


class TestSystemPrompts:
    """Test UPL-compliant system prompts."""
    
    def test_system_prompt_no_legal_advice(self):
        """Test system prompt does NOT contain 'legal advice' language."""
        prompt = get_system_prompt('sk')
        
        # Should NOT contain these forbidden phrases
        forbidden = [
            "právne poradenstvo",  # legal advice
            "právny konzultant",   # legal consultant
            "právne zastupovanie"  # legal representation
        ]
        
        for phrase in forbidden:
            assert phrase not in prompt.lower(), f"Prompt contains forbidden phrase: {phrase}"
    
    def test_system_prompt_has_safe_zone(self):
        """Test system prompt includes safe zone guidelines."""
        prompt = get_system_prompt('sk')
        assert "Safe Zone" in prompt or "ČO MÔŽEŠ ROBIŤ" in prompt
        assert "✅" in prompt  # Has allowed actions
        assert "❌" in prompt  # Has forbidden actions
    
    def test_system_prompt_has_mandatory_rules(self):
        """Test system prompt includes mandatory UPL rules."""
        prompt = get_system_prompt('sk')
        assert "POVINNÉ PRAVIDLÁ" in prompt or "MANDATORY" in prompt
        assert "disclaimerom" in prompt or "disclaimer" in prompt


class TestDisclaimerInjection:
    """Test disclaimer injection into AI responses."""
    
    def test_inject_disclaimer_prepends(self):
        """Test disclaimer is prepended to response."""
        response = "Tu je odpoveď na vašu otázku."
        result = inject_disclaimer(response, 'sk')
        
        assert result.startswith("⚠️")
        assert "CODEX nie je právnická firma" in result
        assert "Tu je odpoveď" in result
    
    def test_inject_disclaimer_no_duplicate(self):
        """Test disclaimer is not duplicated if already present."""
        disclaimer = get_disclaimer('sk')
        response = f"{disclaimer}\n\nTu je odpoveď."
        result = inject_disclaimer(response, 'sk')
        
        # Should not have duplicate disclaimer
        assert result.count("⚠️") == 1
    
    def test_inject_disclaimer_multilingual(self):
        """Test disclaimer injection works for all languages."""
        response = "This is a response."
        languages = ['sk', 'en', 'uk', 'ru', 'de']
        
        for lang in languages:
            result = inject_disclaimer(response, lang)
            assert "⚠️" in result
            assert "This is a response" in result


class TestResponseValidation:
    """Test AI response compliance validation."""
    
    def test_validate_compliant_response(self):
        """Test validation of compliant response."""
        response = """⚠️ CODEX nie je právnická firma a neposkytuje právne poradenstvo.

Všeobecne, na Slovensku Občiansky zákonník upravuje zmluvy v §§ 34-51. 
Pre posúdenie vášho konkrétneho prípadu odporúčam konzultáciu s advokátom."""
        
        result = validate_compliance(response, 'sk')
        assert result['is_compliant'] == True
        assert len(result['violations']) == 0
    
    def test_validate_non_compliant_response(self):
        """Test validation detects UPL violations."""
        response = """Vy by ste mali podať žalobu. Váš prípad je silný a určite vyhráte súd."""
        
        result = validate_compliance(response, 'sk')
        assert result['is_compliant'] == False
        assert len(result['violations']) > 0
    
    def test_validate_warns_missing_disclaimer(self):
        """Test validation warns about missing disclaimer."""
        response = "Tu je odpoveď bez disclaimeru."
        
        result = validate_compliance(response, 'sk')
        assert len(result['warnings']) > 0
        assert any('disclaimer' in w.lower() for w in result['warnings'])


class TestLanguageDetection:
    """Test language detection from query text."""
    
    def test_detect_slovak(self):
        """Test Slovak language detection."""
        text = "Aké sú podmienky platnosti zmluvy na Slovensku?"
        lang = UPLCompliance.detect_language(text)
        assert lang == 'sk'
    
    def test_detect_english(self):
        """Test English language detection."""
        text = "What are the legal requirements for a contract?"
        lang = UPLCompliance.detect_language(text)
        assert lang == 'en'
    
    def test_detect_ukrainian(self):
        """Test Ukrainian language detection."""
        text = "Які мої права згідно з законом України?"
        lang = UPLCompliance.detect_language(text)
        assert lang == 'uk'


class TestDocumentDisclaimers:
    """Test document generation disclaimers."""
    
    def test_document_disclaimer_exists(self):
        """Test document disclaimer exists for all languages."""
        languages = ['sk', 'en', 'uk', 'ru', 'de', 'it', 'fr', 'es', 'pl', 'cs']
        
        for lang in languages:
            disclaimer = UPLCompliance.get_document_disclaimer(lang)
            assert len(disclaimer) > 50
            assert "⚠️" in disclaimer
            assert "AI" in disclaimer or "ai" in disclaimer.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
