import sys
import unittest
from unittest.mock import MagicMock
import os

# Mock dependencies
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()
sys.modules['openpyxl.workbook'] = MagicMock()

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from iniciarVentaW import normalizar_texto

class TestNormalizarTexto(unittest.TestCase):

    def test_none_input(self):
        """Test that None input returns empty string"""
        self.assertEqual(normalizar_texto(None), "")

    def test_empty_string(self):
        """Test that empty string input returns empty string"""
        self.assertEqual(normalizar_texto(""), "")

    def test_nan_string(self):
        """Test that 'nan' string (case insensitive) returns empty string"""
        self.assertEqual(normalizar_texto("nan"), "")
        self.assertEqual(normalizar_texto("NAN"), "")
        self.assertEqual(normalizar_texto("NaN"), "")

    def test_basic_string(self):
        """Test basic string normalization (uppercase, strip)"""
        self.assertEqual(normalizar_texto("hola"), "HOLA")
        self.assertEqual(normalizar_texto("  hola  "), "HOLA")

    def test_numbered_prefix(self):
        """Test removal of numbered prefixes like '1 - '"""
        self.assertEqual(normalizar_texto("1 - Test"), "TEST")
        self.assertEqual(normalizar_texto("123-Test"), "TEST")
        self.assertEqual(normalizar_texto("1- Test"), "TEST")
        self.assertEqual(normalizar_texto("01 - Test"), "TEST")
        self.assertEqual(normalizar_texto(" 1 - Test "), "TEST")

    def test_internal_numbers(self):
        """Test that numbers inside the string are preserved"""
        self.assertEqual(normalizar_texto("Test 1 - Test"), "TEST 1 - TEST")

    def test_numeric_input(self):
        """Test that numeric inputs are converted to string"""
        self.assertEqual(normalizar_texto(123), "123")
        self.assertEqual(normalizar_texto(123.45), "123.45")

    def test_float_nan(self):
        """Test that float('nan') returns empty string"""
        self.assertEqual(normalizar_texto(float('nan')), "")

    def test_just_prefix(self):
        """Test string with just a prefix"""
        self.assertEqual(normalizar_texto("1 - "), "")

if __name__ == '__main__':
    unittest.main()
