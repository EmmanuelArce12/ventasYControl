import unittest
from unittest.mock import MagicMock
import sys

# Mock dependencies before importing the module to avoid import errors
sys.modules['pyodbc'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

# Import the function to test
from iniciarVentaW import normalizar_texto

class TestNormalizarTexto(unittest.TestCase):

    def test_empty_string(self):
        """Test with an empty string."""
        self.assertEqual(normalizar_texto(""), "")

    def test_none(self):
        """Test with None."""
        self.assertEqual(normalizar_texto(None), "")

    def test_nan(self):
        """Test with 'nan' or 'NaN' strings."""
        self.assertEqual(normalizar_texto("nan"), "")
        self.assertEqual(normalizar_texto("NaN"), "")
        self.assertEqual(normalizar_texto("NAN"), "")

    def test_normal_text(self):
        """Test with normal text, ensuring it is converted to uppercase."""
        self.assertEqual(normalizar_texto("test"), "TEST")
        self.assertEqual(normalizar_texto("Test"), "TEST")
        self.assertEqual(normalizar_texto("TEST"), "TEST")

    def test_text_with_spaces(self):
        """Test with leading/trailing spaces."""
        self.assertEqual(normalizar_texto("  test  "), "TEST")
        self.assertEqual(normalizar_texto(" test"), "TEST")
        self.assertEqual(normalizar_texto("test "), "TEST")

    def test_prefix_removal(self):
        """Test removal of numeric prefixes like '1 - ', '23-', etc."""
        self.assertEqual(normalizar_texto("1 - Test"), "TEST")
        self.assertEqual(normalizar_texto("23 - Test"), "TEST")
        self.assertEqual(normalizar_texto("123 - Test"), "TEST")
        self.assertEqual(normalizar_texto("1-Test"), "TEST")
        self.assertEqual(normalizar_texto("12-Test"), "TEST")
        self.assertEqual(normalizar_texto("0 - Test"), "TEST")

    def test_prefix_removal_variations(self):
        """Test variations of prefix formatting."""
        self.assertEqual(normalizar_texto("1   -   Test"), "TEST")
        self.assertEqual(normalizar_texto("1- Test"), "TEST")
        self.assertEqual(normalizar_texto("1 -Test"), "TEST")

    def test_numeric_input(self):
        """Test with numeric input (int, float)."""
        self.assertEqual(normalizar_texto(123), "123")
        self.assertEqual(normalizar_texto(123.45), "123.45")
        # 0 and 0.0 are treated as empty because `not 0` is True
        self.assertEqual(normalizar_texto(0), "")
        self.assertEqual(normalizar_texto(0.0), "")

    def test_prefix_not_removed_if_not_at_start(self):
        """Test that numeric patterns are not removed if not at the start."""
        self.assertEqual(normalizar_texto("Test - 1"), "TEST - 1")
        self.assertEqual(normalizar_texto("Test 1 - 2"), "TEST 1 - 2")

    def test_mixed_content(self):
        """Test with mixed content."""
        self.assertEqual(normalizar_texto("1 - 2 - Test"), "2 - TEST") # Wait, regex is ^\d+\s*-\s*
        # "1 - 2 - Test" -> "2 - Test" -> "2 - TEST"
        # The regex replaces ONLY the first occurrence at the start.

    def test_multiple_prefixes(self):
        # Based on the regex r'^\d+\s*-\s*', it only matches one prefix at the start.
        # "1 - 2 - Test" -> "2 - TEST"
        self.assertEqual(normalizar_texto("1 - 2 - Test"), "2 - TEST")

if __name__ == '__main__':
    unittest.main()
