# tests/test_converter.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from smart_time_py.converter import string_to_datetime, datetime_to_string, validate_date_string



def test_string_to_datetime_valid():
    """✅ Testa a conversão correta de string para datetime."""
    date_str = "2025-02-24 14:30:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    expected = datetime(2025, 2, 24, 14, 30, 0)
    assert string_to_datetime(date_str, date_format) == expected


def test_string_to_datetime_invalid():
    """❌ Testa erro ao converter string inválida para datetime."""
    with pytest.raises(ValueError):
        string_to_datetime("2025/02/24", "%Y-%m-%d")


def test_datetime_to_string_valid():
    """✅ Testa a conversão correta de datetime para string."""
    date_obj = datetime(2025, 2, 24, 14, 30, 0)
    date_format = "%d/%m/%Y %H:%M"
    expected = "24/02/2025 14:30"
    assert datetime_to_string(date_obj, date_format) == expected


def test_datetime_to_string_invalid():
    """❌ Testa erro ao passar objeto inválido para datetime_to_string."""
    with pytest.raises(TypeError):
        datetime_to_string("2025-02-24", "%d/%m/%Y")


def test_validate_date_string_valid():
    """✅ Testa validação bem-sucedida de string de data."""
    assert validate_date_string("24/02/2025", "%d/%m/%Y") is True


def test_validate_date_string_invalid():
    """❌ Testa validação falha de string de data com formato incorreto."""
    assert validate_date_string("2025-02-24", "%d/%m/%Y") is False


def test_validate_date_string_empty():
    """⚡ Testa validação falha quando a string está vazia."""
    assert validate_date_string("", "%d/%m/%Y") is False


# 🏃 Para rodar os testes, execute no terminal:
# pytest tests/test_converter.py --maxfail=1 --disable-warnings -v