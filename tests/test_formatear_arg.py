import sys
import unittest
from unittest.mock import MagicMock
import os

# Mock external dependencies
sys.modules["pandas"] = MagicMock()
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["tkinter.ttk"] = MagicMock()
sys.modules["pyodbc"] = MagicMock()
sys.modules["openpyxl"] = MagicMock()
sys.modules["openpyxl.styles"] = MagicMock()

# Append root directory to sys.path to import initiating script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from iniciarVentaW import formatear_arg

class TestFormatearArg(unittest.TestCase):

    def test_positive_float(self):
        # 1234.56 -> +1.234,56
        self.assertEqual(formatear_arg(1234.56), "+1.234,56")

    def test_negative_float(self):
        # -1234.56 -> -1.234,56
        self.assertEqual(formatear_arg(-1234.56), "-1.234,56")

    def test_zero(self):
        # 0 -> 0,00
        # prefix should be "" because 0 is not > 0.001
        self.assertEqual(formatear_arg(0), "0,00")

    def test_small_positive_number(self):
        # 0.0001 -> 0,00
        # prefix should be "" because 0.0001 is not > 0.001
        self.assertEqual(formatear_arg(0.0001), "0,00")

    def test_integers(self):
        # 1000 -> +1.000,00
        self.assertEqual(formatear_arg(1000), "+1.000,00")

    def test_decimal_less_than_one(self):
        # 0.5 -> +0,50
        self.assertEqual(formatear_arg(0.5), "+0,50")

    def test_negative_decimal_greater_than_minus_one(self):
        # -0.5 -> -0,50
        self.assertEqual(formatear_arg(-0.5), "-0,50")

if __name__ == '__main__':
    unittest.main()
