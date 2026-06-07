import pytest
from src.data.preprocess import clean_text

def test_clean_text_basic():
    raw = "¡Hola! ¿Me cobraron doble este mes, qué hago 123?"
    cleaned = clean_text(raw)
    
    # Verificamos que se hayan eliminado números y puntuación
    assert "cobraron" in cleaned
    assert "123" not in cleaned
    assert "!" not in cleaned

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""
