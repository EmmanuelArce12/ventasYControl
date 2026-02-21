import unittest
from unittest.mock import MagicMock
import sys
import os

# ------------------------------------------------------------
# 1. Mock dependencies BEFORE importing iniciarVentaW
# ------------------------------------------------------------
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()

# Mock openpyxl
mock_openpyxl = MagicMock()
mock_openpyxl.Workbook = MagicMock
sys.modules['openpyxl'] = mock_openpyxl

# Mock openpyxl.styles
mock_styles = MagicMock()
mock_styles.Font = MagicMock
mock_styles.PatternFill = MagicMock
mock_styles.Alignment = MagicMock
mock_styles.Border = MagicMock
mock_styles.Side = MagicMock
sys.modules['openpyxl.styles'] = mock_styles

sys.modules['pandas'] = MagicMock()

# ------------------------------------------------------------
# 2. Import module under test
# ------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to wrap the import in try-except in case there are other import errors,
# although mocking should handle most.
try:
    from iniciarVentaW import limpiar_texto_monetario
except ImportError as e:
    # If this fails, the test cannot run. But we want to see the error.
    raise e

class TestLimpiarTextoMonetario(unittest.TestCase):
    def test_none(self):
        """Test with None input."""
        self.assertEqual(limpiar_texto_monetario(None), "")

    def test_basic_number(self):
        """Test with simple numeric strings and integers."""
        self.assertEqual(limpiar_texto_monetario("123"), "123")
        self.assertEqual(limpiar_texto_monetario(123), "123")

    def test_with_promo_prefix(self):
        """Test with prefix text."""
        self.assertEqual(limpiar_texto_monetario("$1.200 promo"), "1.200")

    def test_with_promo_suffix(self):
        """Test with suffix text and negative sign."""
        self.assertEqual(limpiar_texto_monetario("promo -500"), "-500")

    def test_desc_prefix(self):
        """Test with 'DESC' prefix."""
        self.assertEqual(limpiar_texto_monetario("DESC $300"), "300")

    def test_negative_number(self):
        """Test with negative number."""
        self.assertEqual(limpiar_texto_monetario("-500"), "-500")

    def test_decimal_comma(self):
        """Test with decimal comma."""
        self.assertEqual(limpiar_texto_monetario("12,50"), "12,50")

    def test_decimal_dot(self):
        """Test with decimal dot."""
        self.assertEqual(limpiar_texto_monetario("12.50"), "12.50")

    def test_thousands_separator_simple(self):
        """Test with thousands separator."""
        self.assertEqual(limpiar_texto_monetario("1.200"), "1.200")

    def test_complex_string_thousands_and_decimals(self):
        """Test with thousands separator AND decimals (e.g. 1.234,56)."""
        # This currently fails with the regex r'-?\d+[.,]?\d*' which captures '1.234' only.
        # We expect '1.234,56' to be returned so it can be parsed later.
        self.assertEqual(limpiar_texto_monetario("1.234,56"), "1.234,56")

    def test_complex_string_multiple_thousands(self):
        """Test with multiple thousands separators (e.g. 1.234.567)."""
        self.assertEqual(limpiar_texto_monetario("1.234.567"), "1.234.567")

if __name__ == '__main__':
    unittest.main()
