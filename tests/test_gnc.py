import unittest
import sys
from unittest.mock import MagicMock
import os

# Mock dependencies before importing modules that use them
sys.modules["pandas"] = MagicMock()
sys.modules["pyodbc"] = MagicMock()
sys.modules["openpyxl"] = MagicMock()
sys.modules["openpyxl.styles"] = MagicMock()
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["tkinter.ttk"] = MagicMock()

# Add root directory to path to import iniciarVentaW
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import iniciarVentaW

class TestGNC(unittest.TestCase):

    def test_aforador_consumo(self):
        # Normal case
        af = iniciarVentaW.AforadorGNC(100, 200, 10)
        self.assertEqual(af.consumo(), 100)
        self.assertEqual(af.total(), 1000)

    def test_aforador_negative_consumo(self):
        # Negative consumption (final < inicial) should be 0
        af = iniciarVentaW.AforadorGNC(200, 100, 10)
        self.assertEqual(af.consumo(), 0)
        self.assertEqual(af.total(), 0)

    def test_cobertura_empty(self):
        # Empty list of aforadores
        cob = iniciarVentaW.CoberturaGNC("Test", "Resp", [])
        self.assertEqual(cob.total(), 0)

    def test_cobertura_single(self):
        # Single aforador
        af = iniciarVentaW.AforadorGNC(100, 200, 10) # total 1000
        cob = iniciarVentaW.CoberturaGNC("Test", "Resp", [af])
        self.assertEqual(cob.total(), 1000)

    def test_cobertura_multiple(self):
        # Multiple aforadores
        af1 = iniciarVentaW.AforadorGNC(100, 200, 10) # 1000
        af2 = iniciarVentaW.AforadorGNC(50, 100, 20)  # 50 * 20 = 1000
        cob = iniciarVentaW.CoberturaGNC("Test", "Resp", [af1, af2])
        self.assertEqual(cob.total(), 2000)

    def test_cobertura_with_mocked_aforador(self):
        # Strict unit test with mock
        mock_af = MagicMock()
        mock_af.total.return_value = 500
        cob = iniciarVentaW.CoberturaGNC("Test", "Resp", [mock_af])
        self.assertEqual(cob.total(), 500)
        mock_af.total.assert_called_once()

if __name__ == '__main__':
    unittest.main()
