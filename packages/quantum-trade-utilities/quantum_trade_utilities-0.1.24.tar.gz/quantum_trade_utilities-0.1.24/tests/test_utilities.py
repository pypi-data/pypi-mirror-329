import pytest
from quantum_trade_utilities.core.propcase import propcase

def test_propcase():
    """Test basic text cleaning functionality"""
    input_text = "hello"
    expected = "Hello"
    assert propcase(input_text) == expected