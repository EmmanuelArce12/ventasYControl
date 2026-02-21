import unittest
from iniciarVentaW import parse_moneda_robusto

class TestParseMonedaRobusto(unittest.TestCase):

    def test_null_and_empty(self):
        self.assertEqual(parse_moneda_robusto(None), 0.0)
        self.assertEqual(parse_moneda_robusto(""), 0.0)
        self.assertEqual(parse_moneda_robusto("   "), 0.0)
        self.assertEqual(parse_moneda_robusto("nan"), 0.0)
        self.assertEqual(parse_moneda_robusto("NaN"), 0.0)
        self.assertEqual(parse_moneda_robusto("NAN"), 0.0)

    def test_numeric_types(self):
        self.assertEqual(parse_moneda_robusto(100), 100.0)
        self.assertEqual(parse_moneda_robusto(100.5), 100.5)
        self.assertEqual(parse_moneda_robusto(0), 0.0)
        self.assertEqual(parse_moneda_robusto(-50.5), -50.5)

    def test_basic_strings(self):
        self.assertEqual(parse_moneda_robusto("100"), 100.0)
        self.assertEqual(parse_moneda_robusto("100.5"), 100.5)
        self.assertEqual(parse_moneda_robusto("-100.5"), -100.5)

    def test_currency_symbols(self):
        self.assertEqual(parse_moneda_robusto("$100"), 100.0)
        self.assertEqual(parse_moneda_robusto("$ 100"), 100.0)
        self.assertEqual(parse_moneda_robusto("100$"), 100.0)
        self.assertEqual(parse_moneda_robusto(" $ 100 "), 100.0)
        self.assertEqual(parse_moneda_robusto("$-100"), -100.0)

    def test_argentine_format(self):
        # dot for thousands, comma for decimal
        self.assertEqual(parse_moneda_robusto("1.234,56"), 1234.56)
        self.assertEqual(parse_moneda_robusto("1.000.000,00"), 1000000.0)
        self.assertEqual(parse_moneda_robusto("10.000,50"), 10000.50)

    def test_us_format(self):
        # comma for thousands, dot for decimal
        self.assertEqual(parse_moneda_robusto("1,234.56"), 1234.56)
        self.assertEqual(parse_moneda_robusto("1,000,000.00"), 1000000.0)
        self.assertEqual(parse_moneda_robusto("10,000.50"), 10000.50)

    def test_mixed_ambiguous(self):
        # Comma only -> treated as decimal
        self.assertEqual(parse_moneda_robusto("1234,56"), 1234.56)
        self.assertEqual(parse_moneda_robusto(",50"), 0.50)

        # Dot only -> treated as normal float
        self.assertEqual(parse_moneda_robusto("1234.56"), 1234.56)

        # Ambiguous case: "1.234" -> Is it 1234 or 1.234?
        # The function logic:
        # if ',' in s and '.' in s: ...
        # elif ',' in s: replace , with .
        # else: float(s)
        # So "1.234" goes to float("1.234") -> 1.234
        self.assertEqual(parse_moneda_robusto("1.234"), 1.234)

        # "1,234" -> elif ',' in s -> replace , with . -> 1.234
        self.assertEqual(parse_moneda_robusto("1,234"), 1.234)

    def test_invalid_inputs(self):
        self.assertEqual(parse_moneda_robusto("abc"), 0.0)
        self.assertEqual(parse_moneda_robusto("hello"), 0.0)
        self.assertEqual(parse_moneda_robusto("12.34.56"), 0.0) # Invalid float format

    def test_edge_cases_spaces(self):
         self.assertEqual(parse_moneda_robusto(" 1 0 0 "), 100.0)
         self.assertEqual(parse_moneda_robusto("1. 000, 00"), 1000.0)

if __name__ == '__main__':
    unittest.main()
