import sys
import unittest
from unittest.mock import MagicMock

# Mock dependencies before import
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()

# Now import the target module
# Use absolute import because current directory is in sys.path
import iniciarVentaW
from iniciarVentaW import formatear_arg

class TestFormatearArg(unittest.TestCase):
    def test_positive_float(self):
        self.assertEqual(formatear_arg(1234.56), "+1.234,56")

    def test_negative_float(self):
        self.assertEqual(formatear_arg(-1234.56), "-1.234,56")

    def test_zero(self):
        self.assertEqual(formatear_arg(0), "0,00")

    def test_small_positive_just_above_threshold(self):
        # 0.002 > 0.001 -> has plus sign
        self.assertEqual(formatear_arg(0.002), "+0,00")

    def test_small_positive_at_threshold(self):
        # 0.001 is not > 0.001 -> no plus sign
        self.assertEqual(formatear_arg(0.001), "0,00")

    def test_small_positive_below_threshold(self):
        # 0.0001 is not > 0.001 -> no plus sign
        self.assertEqual(formatear_arg(0.0001), "0,00")

    def test_large_number(self):
        self.assertEqual(formatear_arg(1000000.00), "+1.000.000,00")

    def test_rounding_up(self):
        self.assertEqual(formatear_arg(10.556), "+10,56")

    def test_rounding_down(self):
        self.assertEqual(formatear_arg(10.554), "+10,55")

    def test_integer(self):
        self.assertEqual(formatear_arg(100), "+100,00")
        self.assertEqual(formatear_arg(-100), "-100,00")

if __name__ == '__main__':
    unittest.main()
