import sys
from unittest.mock import MagicMock

# Mock pyodbc before importing the module
sys.modules["pyodbc"] = MagicMock()

import unittest
from iniciarVentaW import parse_moneda_robusto

class TestParseMonedaRobusto(unittest.TestCase):

    def test_null_empty_nan(self):
        """Test handling of None, empty strings, and 'nan'."""
        self.assertEqual(parse_moneda_robusto(None), 0.0)
        self.assertEqual(parse_moneda_robusto(""), 0.0)
        self.assertEqual(parse_moneda_robusto("   "), 0.0)
        self.assertEqual(parse_moneda_robusto("nan"), 0.0)
        self.assertEqual(parse_moneda_robusto("NaN"), 0.0)
        self.assertEqual(parse_moneda_robusto("NAN"), 0.0)

    def test_numeric_types(self):
        """Test handling of integers and floats."""
        self.assertEqual(parse_moneda_robusto(100), 100.0)
        self.assertEqual(parse_moneda_robusto(100.5), 100.5)
        self.assertEqual(parse_moneda_robusto(0), 0.0)
        self.assertEqual(parse_moneda_robusto(-50), -50.0)

    def test_basic_string_numbers(self):
        """Test simple numeric strings."""
        self.assertEqual(parse_moneda_robusto("123"), 123.0)
        self.assertEqual(parse_moneda_robusto("123.45"), 123.45)
        self.assertEqual(parse_moneda_robusto("-123.45"), -123.45)

    def test_currency_symbols_and_spacing(self):
        """Test removal of '$' and spaces."""
        self.assertEqual(parse_moneda_robusto("$100"), 100.0)
        self.assertEqual(parse_moneda_robusto("$ 100"), 100.0)
        self.assertEqual(parse_moneda_robusto("100$"), 100.0)
        self.assertEqual(parse_moneda_robusto(" $ 100 "), 100.0)
        self.assertEqual(parse_moneda_robusto("$1,234.56"), 1234.56)

    def test_argentine_format(self):
        """Test Argentine format (dot as thousands separator, comma as decimal)."""
        # 1.234,56 -> 1234.56
        self.assertEqual(parse_moneda_robusto("1.234,56"), 1234.56)
        # 1.000.000,00 -> 1000000.00
        self.assertEqual(parse_moneda_robusto("1.000.000,00"), 1000000.00)
        # 15.400,50
        self.assertEqual(parse_moneda_robusto("15.400,50"), 15400.50)

    def test_us_format(self):
        """Test US format (comma as thousands separator, dot as decimal)."""
        # 1,234.56 -> 1234.56
        self.assertEqual(parse_moneda_robusto("1,234.56"), 1234.56)
        # 1,000,000.00 -> 1000000.00
        self.assertEqual(parse_moneda_robusto("1,000,000.00"), 1000000.00)

    def test_mixed_ambiguous(self):
        """Test ambiguous cases or single separator cases."""
        # Comma as decimal
        self.assertEqual(parse_moneda_robusto("123,45"), 123.45)
        # Dot as decimal
        self.assertEqual(parse_moneda_robusto("123.45"), 123.45)
        # Thousands separator only (Arg) - e.g. 1.200 (could be 1200 or 1.2)
        # The logic: if ',' in s and '.' in s: ...
        # elif ',' in s: replace ',' with '.'
        # else: float(s)
        # So "1.200" becomes float("1.200") -> 1.2.
        # This might be an ambiguity in the function, but I am testing existing behavior.
        self.assertEqual(parse_moneda_robusto("1.200"), 1.2)

        # Comma only -> decimal
        self.assertEqual(parse_moneda_robusto("1200,50"), 1200.50)

    def test_invalid_inputs(self):
        """Test non-numeric strings that should be handled gracefully."""
        self.assertEqual(parse_moneda_robusto("abc"), 0.0)
        self.assertEqual(parse_moneda_robusto("hello world"), 0.0)
        self.assertEqual(parse_moneda_robusto("12.34.56"), 0.0) # multiple dots, no commas -> invalid float

    def test_edge_cases(self):
        """Test edge cases."""
        # Negative argentine
        self.assertEqual(parse_moneda_robusto("-1.234,56"), -1234.56)
        # Negative US
        self.assertEqual(parse_moneda_robusto("-1,234.56"), -1234.56)
        # Large numbers
        self.assertEqual(parse_moneda_robusto("999.999.999,99"), 999999999.99)

if __name__ == '__main__':
    unittest.main()
