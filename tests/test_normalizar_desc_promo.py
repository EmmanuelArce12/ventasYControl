import sys
import unittest
from unittest.mock import MagicMock

# Mock dependencies before importing iniciarVentaW
sys.modules["pandas"] = MagicMock()
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["tkinter.ttk"] = MagicMock()
sys.modules["pyodbc"] = MagicMock()
sys.modules["openpyxl"] = MagicMock()
sys.modules["openpyxl.styles"] = MagicMock()

# Now import the function to be tested
# We need to add the parent directory to sys.path if running from tests/
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from iniciarVentaW import normalizar_desc_promo

class TestNormalizarDescPromo(unittest.TestCase):

    def test_none_empty(self):
        """Test with None, empty string, and whitespace."""
        self.assertEqual(normalizar_desc_promo(None), 0.0)
        self.assertEqual(normalizar_desc_promo(""), 0.0)
        self.assertEqual(normalizar_desc_promo("   "), 0.0)

    def test_simple_integers(self):
        """Test simple integer strings."""
        self.assertEqual(normalizar_desc_promo("100"), 100.0)
        self.assertEqual(normalizar_desc_promo("0"), 0.0)
        self.assertEqual(normalizar_desc_promo("50"), 50.0)

    def test_simple_floats(self):
        """Test simple float strings."""
        self.assertEqual(normalizar_desc_promo("10.50"), 10.5)
        self.assertEqual(normalizar_desc_promo("0.99"), 0.99)
        # 10,50 -> comma as decimal separator
        self.assertEqual(normalizar_desc_promo("10,50"), 10.5)

    def test_thousands_separator_arg(self):
        """Test Argentine/European format (1.234,56)."""
        self.assertEqual(normalizar_desc_promo("1.234,56"), 1234.56)
        self.assertEqual(normalizar_desc_promo("1.000"), 1000.0)
        self.assertEqual(normalizar_desc_promo("1.200"), 1200.0)
        self.assertEqual(normalizar_desc_promo("10.000,00"), 10000.0)

    def test_thousands_separator_us(self):
        """Test US/UK format (1,234.56)."""
        self.assertEqual(normalizar_desc_promo("1,234.56"), 1234.56)
        self.assertEqual(normalizar_desc_promo("1,000"), 1000.0)
        self.assertEqual(normalizar_desc_promo("1,200"), 1200.0)
        self.assertEqual(normalizar_desc_promo("10,000.00"), 10000.0)

    def test_ambiguous_thousands(self):
        """Test ambiguous cases where dot/comma could be decimal or thousand separator."""
        # The function assumes 3 digits after dot/comma means thousands separator
        self.assertEqual(normalizar_desc_promo("1.234"), 1234.0)
        self.assertEqual(normalizar_desc_promo("1,234"), 1234.0)

        # But if not exactly 3 digits, it's decimal
        self.assertEqual(normalizar_desc_promo("1.23"), 1.23)
        self.assertEqual(normalizar_desc_promo("1,23"), 1.23)
        self.assertEqual(normalizar_desc_promo("1.2"), 1.2)
        self.assertEqual(normalizar_desc_promo("1,2"), 1.2)

    def test_mixed_text(self):
        """Test text mixed with numbers."""
        self.assertEqual(normalizar_desc_promo("Promo $500 off"), 500.0)
        self.assertEqual(normalizar_desc_promo("Desc 10%"), 10.0)
        self.assertEqual(normalizar_desc_promo("Total: 1.200,50"), 1200.50)
        self.assertEqual(normalizar_desc_promo("abc 123 def"), 123.0)

    def test_multiple_numbers(self):
        """Test strings containing multiple numbers."""
        # Should sum them up
        self.assertEqual(normalizar_desc_promo("Promo $100 + $200"), 300.0)
        self.assertEqual(normalizar_desc_promo("10, 20, 30"), 60.0)
        self.assertEqual(normalizar_desc_promo("1.5 + 2.5"), 4.0)

    def test_edge_cases(self):
        """Test edge cases."""
        # Just separators
        self.assertEqual(normalizar_desc_promo("."), 0.0)
        self.assertEqual(normalizar_desc_promo(","), 0.0)
        # Weird formats
        self.assertEqual(normalizar_desc_promo("1..2"), 0.0) # regex might pick 1..2 as 1..2 -> invalid float
        self.assertEqual(normalizar_desc_promo("1,,2"), 0.0) # same

if __name__ == '__main__':
    unittest.main()
