import sys
import unittest
from unittest.mock import MagicMock

# ----------------------------------------------------------------------------------
# 1. MOCK DEPENDENCIES
# ----------------------------------------------------------------------------------
# We mock these modules because they are not installed in the environment
# and we only want to test the logic of calcular_gnc_general.
sys.modules['pandas'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

# ----------------------------------------------------------------------------------
# 2. IMPORT MODULE UNDER TEST
# ----------------------------------------------------------------------------------
import iniciarVentaW

class TestGNCGeneral(unittest.TestCase):

    def test_empty_list(self):
        """Test that an empty list returns 0."""
        result = iniciarVentaW.calcular_gnc_general([])
        self.assertEqual(result, 0)

    def test_single_aforador(self):
        """Test calculation for a single aforador."""
        # Aforador(inicial, final, precio)
        # Consumo = 200 - 100 = 100
        # Total = 100 * 10 = 1000
        a = iniciarVentaW.AforadorGNC(100, 200, 10)
        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertEqual(result, 1000)

    def test_multiple_aforadores(self):
        """Test calculation for multiple aforadores."""
        # A1: (100, 200, 10) -> 100 * 10 = 1000
        # A2: (500, 600, 20) -> 100 * 20 = 2000
        # Total = 3000
        a1 = iniciarVentaW.AforadorGNC(100, 200, 10)
        a2 = iniciarVentaW.AforadorGNC(500, 600, 20)
        result = iniciarVentaW.calcular_gnc_general([a1, a2])
        self.assertEqual(result, 3000)

    def test_zero_consumption(self):
        """Test when consumption is zero."""
        # A: (100, 100, 10) -> 0 * 10 = 0
        a = iniciarVentaW.AforadorGNC(100, 100, 10)
        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertEqual(result, 0)

    def test_negative_consumption(self):
        """Test when final reading is less than initial (should be 0)."""
        # A: (200, 100, 10) -> max(100 - 200, 0) -> 0 * 10 = 0
        a = iniciarVentaW.AforadorGNC(200, 100, 10)
        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertEqual(result, 0)

    def test_custom_price(self):
        """Test with custom price."""
        # A: (0, 10, 50) -> 10 * 50 = 500
        a = iniciarVentaW.AforadorGNC(0, 10, 50)
        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertEqual(result, 500)

    def test_none_initialization(self):
        """Test initialization with None values."""
        # Should default to 0.0
        a = iniciarVentaW.AforadorGNC(None, None, None)
        # Consumo = 0 - 0 = 0
        # Total = 0 * default_price
        self.assertEqual(a.inicial, 0.0)
        self.assertEqual(a.final, 0.0)
        # default price is 669 in iniciarVentaW.py
        self.assertEqual(a.precio, 669.0)

        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertEqual(result, 0)

    def test_float_values(self):
        """Test with float values."""
        # A: (10.5, 20.5, 1.5) -> 10.0 * 1.5 = 15.0
        a = iniciarVentaW.AforadorGNC(10.5, 20.5, 1.5)
        result = iniciarVentaW.calcular_gnc_general([a])
        self.assertAlmostEqual(result, 15.0)

if __name__ == '__main__':
    unittest.main()
