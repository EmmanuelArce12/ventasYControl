import unittest
import sys
import os
from unittest.mock import MagicMock

# Mock pyodbc before importing iniciarVentaW because the shared library is missing
sys.modules["pyodbc"] = MagicMock()

# Add the repository root to sys.path to allow importing from iniciarVentaW
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iniciarVentaW import AforadorGNC, PRECIO_GNC_DEFAULT

class TestAforadorGNC(unittest.TestCase):

    def test_initialization_defaults(self):
        """Test initialization with default values."""
        aforador = AforadorGNC()
        self.assertEqual(aforador.inicial, 0.0)
        self.assertEqual(aforador.final, 0.0)
        self.assertEqual(aforador.precio, float(PRECIO_GNC_DEFAULT))

    def test_initialization_values(self):
        """Test initialization with specific values."""
        aforador = AforadorGNC(inicial=100.0, final=200.0, precio=10.0)
        self.assertEqual(aforador.inicial, 100.0)
        self.assertEqual(aforador.final, 200.0)
        self.assertEqual(aforador.precio, 10.0)

    def test_consumo_normal(self):
        """Test consumo calculation where final > inicial."""
        aforador = AforadorGNC(inicial=100.0, final=150.0)
        self.assertEqual(aforador.consumo(), 50.0)

    def test_consumo_zero_diff(self):
        """Test consumo calculation where final == inicial."""
        aforador = AforadorGNC(inicial=100.0, final=100.0)
        self.assertEqual(aforador.consumo(), 0.0)

    def test_consumo_negative(self):
        """Test consumo calculation where final < inicial (should return 0)."""
        aforador = AforadorGNC(inicial=150.0, final=100.0)
        self.assertEqual(aforador.consumo(), 0.0)

    def test_total(self):
        """Test total calculation."""
        aforador = AforadorGNC(inicial=100.0, final=150.0, precio=10.0)
        # Consumo = 50, Precio = 10, Total = 500
        self.assertEqual(aforador.total(), 500.0)

    def test_total_default_price(self):
        """Test total calculation with default price."""
        aforador = AforadorGNC(inicial=100.0, final=101.0)
        # Consumo = 1, Precio = PRECIO_GNC_DEFAULT
        self.assertEqual(aforador.total(), float(PRECIO_GNC_DEFAULT))

    def test_input_handling_strings(self):
        """Test initialization with string inputs."""
        aforador = AforadorGNC(inicial="100.5", final="200.5", precio="20.0")
        self.assertEqual(aforador.inicial, 100.5)
        self.assertEqual(aforador.final, 200.5)
        self.assertEqual(aforador.precio, 20.0)

    def test_input_handling_none(self):
        """Test initialization with None values."""
        aforador = AforadorGNC(inicial=None, final=None, precio=None)
        self.assertEqual(aforador.inicial, 0.0)
        self.assertEqual(aforador.final, 0.0)
        self.assertEqual(aforador.precio, float(PRECIO_GNC_DEFAULT))

    def test_input_handling_empty_string(self):
        """Test initialization with empty strings."""
        aforador = AforadorGNC(inicial="", final="", precio="")
        self.assertEqual(aforador.inicial, 0.0)
        self.assertEqual(aforador.final, 0.0)
        self.assertEqual(aforador.precio, float(PRECIO_GNC_DEFAULT))

if __name__ == '__main__':
    unittest.main()
