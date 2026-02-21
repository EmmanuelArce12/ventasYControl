import sys
import os
import unittest
from unittest.mock import MagicMock

# --- MOCKING DEPENDENCIES BEFORE IMPORT ---
sys.modules["pandas"] = MagicMock()
sys.modules["pyodbc"] = MagicMock()
sys.modules["openpyxl"] = MagicMock()
sys.modules["openpyxl.styles"] = MagicMock()
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["tkinter.ttk"] = MagicMock()

# Add parent directory to path to import iniciarVentaW
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the module under test
# We use try-except to handle potential import errors if mocks are not sufficient,
# though MagicMock usually handles it.
try:
    from iniciarVentaW import calcular_gnc_general, AforadorGNC, PRECIO_GNC_DEFAULT
except ImportError as e:
    # Fallback or fail gracefully if import fails
    raise ImportError(f"Failed to import iniciarVentaW: {e}")

class TestGNC(unittest.TestCase):
    def test_empty_list(self):
        """Test with an empty list of aforadores."""
        self.assertEqual(calcular_gnc_general([]), 0.0)

    def test_single_aforador(self):
        """Test with a single aforador with valid consumption."""
        # Consumption: 100, Price: Default (669) -> 66900
        af = AforadorGNC(inicial=1000, final=1100)
        expected = 100 * PRECIO_GNC_DEFAULT
        self.assertEqual(calcular_gnc_general([af]), expected)

    def test_multiple_aforadores(self):
        """Test with multiple aforadores."""
        # Af1: Cons 10 * 669 = 6690
        # Af2: Cons 20 * 669 = 13380
        # Total: 20070
        af1 = AforadorGNC(inicial=1000, final=1010)
        af2 = AforadorGNC(inicial=2000, final=2020)
        expected = (10 + 20) * PRECIO_GNC_DEFAULT
        self.assertEqual(calcular_gnc_general([af1, af2]), expected)

    def test_zero_consumption(self):
        """Test aforador with zero consumption."""
        af = AforadorGNC(inicial=1000, final=1000)
        self.assertEqual(calcular_gnc_general([af]), 0.0)

    def test_negative_consumption(self):
        """Test aforador with negative consumption (final < initial)."""
        # Should be treated as 0 consumption
        af = AforadorGNC(inicial=1100, final=1000)
        self.assertEqual(calcular_gnc_general([af]), 0.0)

    def test_custom_price(self):
        """Test aforador with a custom price."""
        custom_price = 500.0
        af = AforadorGNC(inicial=1000, final=1010, precio=custom_price)
        expected = 10 * custom_price
        self.assertEqual(calcular_gnc_general([af]), expected)

if __name__ == "__main__":
    unittest.main()
