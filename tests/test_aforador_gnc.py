import sys
import os
import unittest
from unittest.mock import MagicMock

# Mock external dependencies
# We mock them BEFORE importing iniciarVentaW
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()

# Add parent directory to path to import iniciarVentaW
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import iniciarVentaW

class TestAforadorGNC(unittest.TestCase):

    def test_init_default(self):
        """Test initialization with default values."""
        aforador = iniciarVentaW.AforadorGNC()
        self.assertEqual(aforador.inicial, 0.0)
        self.assertEqual(aforador.final, 0.0)
        self.assertEqual(aforador.precio, iniciarVentaW.PRECIO_GNC_DEFAULT)

    def test_init_custom(self):
        """Test initialization with custom values."""
        aforador = iniciarVentaW.AforadorGNC(100.0, 200.0, 50.0)
        self.assertEqual(aforador.inicial, 100.0)
        self.assertEqual(aforador.final, 200.0)
        self.assertEqual(aforador.precio, 50.0)

    def test_init_with_none(self):
        """Test initialization with None values."""
        aforador = iniciarVentaW.AforadorGNC(None, None, None)
        self.assertEqual(aforador.inicial, 0.0)
        self.assertEqual(aforador.final, 0.0)
        self.assertEqual(aforador.precio, iniciarVentaW.PRECIO_GNC_DEFAULT)

    def test_consumo(self):
        """Test consumption calculation."""
        aforador = iniciarVentaW.AforadorGNC(100.0, 200.0)
        self.assertEqual(aforador.consumo(), 100.0)

    def test_consumo_negative(self):
        """Test consumption calculation when final < initial."""
        # Should return 0 if final < inicial
        aforador = iniciarVentaW.AforadorGNC(200.0, 100.0)
        self.assertEqual(aforador.consumo(), 0.0)

    def test_consumo_zero(self):
        """Test consumption calculation when final == initial."""
        aforador = iniciarVentaW.AforadorGNC(100.0, 100.0)
        self.assertEqual(aforador.consumo(), 0.0)

    def test_total(self):
        """Test total cost calculation."""
        aforador = iniciarVentaW.AforadorGNC(100.0, 200.0, 10.0)
        self.assertEqual(aforador.total(), 1000.0)

    def test_total_default_price(self):
        """Test total cost calculation with default price."""
        aforador = iniciarVentaW.AforadorGNC(100.0, 200.0)
        expected_total = 100.0 * iniciarVentaW.PRECIO_GNC_DEFAULT
        self.assertEqual(aforador.total(), expected_total)

if __name__ == '__main__':
    unittest.main()
