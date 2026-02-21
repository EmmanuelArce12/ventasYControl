import sys
import os
from unittest.mock import MagicMock
import pytest

# Add parent directory to path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies that are not available or problematic
# We mock them BEFORE importing the module under test
mock_modules = [
    "pyodbc",
    "tkinter",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "tkinter.simpledialog",
    "tkinter.ttk"
]

for module in mock_modules:
    sys.modules[module] = MagicMock()

# Now import the target module
from iniciarVentaW import normalizar_desc_promo

class TestNormalizarDescPromo:

    def test_empty_input(self):
        """Test with None, empty string, or 0."""
        assert normalizar_desc_promo(None) == 0.0
        assert normalizar_desc_promo("") == 0.0
        assert normalizar_desc_promo(0) == 0.0

    def test_no_numbers(self):
        """Test strings with no numbers."""
        assert normalizar_desc_promo("Descuento promo") == 0.0
        assert normalizar_desc_promo("Promo especial") == 0.0

    def test_simple_integers(self):
        """Test simple integer values."""
        assert normalizar_desc_promo("Descuento 100") == 100.0
        assert normalizar_desc_promo("Promo 50") == 50.0

    def test_argentine_format(self):
        """Test Argentine/European format: 1.234,56"""
        # Thousands separator dot, decimal comma
        assert normalizar_desc_promo("Promo 1.200,50") == 1200.50
        # Thousands separator dot only
        assert normalizar_desc_promo("Promo 1.000") == 1000.0
        # Decimal comma only
        assert normalizar_desc_promo("Promo 50,5") == 50.5
        assert normalizar_desc_promo("Promo 100,00") == 100.0

    def test_usa_format(self):
        """Test USA format: 1,234.56"""
        # Thousands separator comma, decimal dot
        assert normalizar_desc_promo("Promo 1,200.50") == 1200.50
        # Thousands separator comma only
        assert normalizar_desc_promo("Promo 1,000") == 1000.0
        # Decimal dot only
        assert normalizar_desc_promo("Promo 50.5") == 50.5
        assert normalizar_desc_promo("Promo 100.00") == 100.0

    def test_multiple_numbers(self):
        """Test extraction and summation of multiple numbers."""
        assert normalizar_desc_promo("Promo 100 y 200") == 300.0
        assert normalizar_desc_promo("Descuento 50 + Bonificación 20") == 70.0

    def test_currency_symbols(self):
        """Test with currency symbols."""
        assert normalizar_desc_promo("$100") == 100.0
        assert normalizar_desc_promo("USD 50") == 50.0
        assert normalizar_desc_promo("Promo $1.200,50") == 1200.50

    def test_negative_numbers(self):
        """
        Test negative numbers.
        Currently the regex r"\d[\d.,]*" does NOT capture the minus sign.
        So -500 becomes 500. This is expected behavior for extracting 'discount amount'.
        """
        assert normalizar_desc_promo("Descuento -500") == 500.0
        assert normalizar_desc_promo("Ajuste -50.50") == 50.50

    def test_mixed_text(self):
        """Test numbers embedded in text."""
        assert normalizar_desc_promo("Promo descuento 500 pesos por pago efectivo") == 500.0
        # "2x1" -> "2", "1". "100" -> 100. Total 103.
        assert normalizar_desc_promo("Promo 2x1 (valor 100)") == 103.0

    def test_unintended_matches(self):
        """Test scenarios that might produce unexpected results due to simple regex."""
        # "2x1" -> "2", "1" -> 3.0
        assert normalizar_desc_promo("Promo 2x1") == 3.0

        # "Calle 123 numero 45" -> 123 + 45 = 168
        assert normalizar_desc_promo("Calle 123 numero 45") == 168.0

    def test_ambiguous_thousands(self):
        """Test ambiguous cases."""
        # "1.234" -> 1234 (Argentine/European assumption for 3 decimals after dot)
        assert normalizar_desc_promo("1.234") == 1234.0

        # "1,234" -> 1234 (USA assumption for 3 decimals after comma)
        assert normalizar_desc_promo("1,234") == 1234.0

        # "1.5" -> 1.5 (Dot is decimal separator if not following 3 digits pattern)
        assert normalizar_desc_promo("1.5") == 1.5

        # "1,5" -> 1.5 (Comma is decimal separator if not following 3 digits pattern)
        assert normalizar_desc_promo("1,5") == 1.5
