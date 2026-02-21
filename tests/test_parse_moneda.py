import sys
import unittest
from unittest.mock import MagicMock

# Mock dependencies before import to avoid runtime errors
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()

# Now import the function to test
from iniciarVentaW import parse_moneda_robusto

class TestParseMoneda(unittest.TestCase):

    def test_basic_types(self):
        """Test integers and floats."""
        self.assertEqual(parse_moneda_robusto(100), 100.0)
        self.assertEqual(parse_moneda_robusto(100.5), 100.5)
        self.assertEqual(parse_moneda_robusto(-50), -50.0)
        self.assertEqual(parse_moneda_robusto(0), 0.0)

    def test_simple_strings(self):
        """Test simple string numbers."""
        self.assertEqual(parse_moneda_robusto("100"), 100.0)
        self.assertEqual(parse_moneda_robusto("100.50"), 100.5)
        self.assertEqual(parse_moneda_robusto("-50.5"), -50.5)

    def test_currency_symbols_and_spaces(self):
        """Test removal of currency symbols and whitespace."""
        self.assertEqual(parse_moneda_robusto("$100"), 100.0)
        self.assertEqual(parse_moneda_robusto("$ 100"), 100.0)
        self.assertEqual(parse_moneda_robusto("100 $"), 100.0)
        self.assertEqual(parse_moneda_robusto("  100  "), 100.0)
        self.assertEqual(parse_moneda_robusto(" $ 100.50 "), 100.5)
        # Spaces inside numbers (handled by replace(" ", ""))
        self.assertEqual(parse_moneda_robusto("1 200"), 1200.0)

    def test_regional_formats_argentina(self):
        """Test Argentina/Europe format (1.234,56)."""
        # Thousands separator '.', decimal separator ','
        self.assertEqual(parse_moneda_robusto("1.234,56"), 1234.56)
        self.assertEqual(parse_moneda_robusto("10.000,00"), 10000.0)
        # Comma decimal only
        self.assertEqual(parse_moneda_robusto("1234,56"), 1234.56)

        # Ambiguous case: "1.200" (Standard Python float parsing treats dot as decimal)
        # This behavior is expected given the implementation relies on float() when only dots are present
        self.assertEqual(parse_moneda_robusto("1.200"), 1.2)

    def test_regional_formats_usa(self):
        """Test USA format (1,234.56)."""
        # Thousands separator ',', decimal separator '.'
        self.assertEqual(parse_moneda_robusto("1,234.56"), 1234.56)
        self.assertEqual(parse_moneda_robusto("10,000.00"), 10000.0)
        # Dot decimal only
        self.assertEqual(parse_moneda_robusto("1234.56"), 1234.56)

        # Ambiguous case: "1,200" (Implementation treats lone comma as decimal separator)
        # This implies "1,200" is parsed as 1.2, consistent with Argentine/European input without dots
        self.assertEqual(parse_moneda_robusto("1,200"), 1.2)

    def test_mixed_separators_large_numbers(self):
        """Test large numbers with multiple separators."""
        # Arg: 1.234.567,89
        self.assertEqual(parse_moneda_robusto("1.234.567,89"), 1234567.89)
        # US: 1,234,567.89
        self.assertEqual(parse_moneda_robusto("1,234,567.89"), 1234567.89)

    def test_negative_formatted(self):
        """Test negative formatted numbers."""
        self.assertEqual(parse_moneda_robusto("-1.234,56"), -1234.56)
        self.assertEqual(parse_moneda_robusto("-$ 1.234,56"), -1234.56)

    def test_edge_cases(self):
        """Test None, NaN, empty strings, invalid."""
        self.assertEqual(parse_moneda_robusto(None), 0.0)
        self.assertEqual(parse_moneda_robusto("nan"), 0.0)
        self.assertEqual(parse_moneda_robusto("NAN"), 0.0)
        self.assertEqual(parse_moneda_robusto(""), 0.0)
        self.assertEqual(parse_moneda_robusto("invalid"), 0.0)
        self.assertEqual(parse_moneda_robusto(object()), 0.0)

if __name__ == '__main__':
    unittest.main()
