import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock sys.modules for tkinter and others to prevent side effects
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()
sys.modules['pandas'] = MagicMock()

# Import the module under test
import iniciarVentaW

class TestPathSecurity(unittest.TestCase):
    def test_obtener_ruta_cierre_caja(self):
        """Test that the path is dynamic and within user directory."""
        path = iniciarVentaW.obtener_ruta_cierre_caja()
        home = os.path.expanduser("~")
        expected_suffix = "cierres de caja"

        self.assertTrue(path.startswith(home), f"Path {path} should start with {home}")
        self.assertTrue(path.endswith(expected_suffix), f"Path {path} should end with {expected_suffix}")

        # On Windows, user path starts with C:\Users, but hardcoded was "C:/cierres de caja/"
        # We want to ensure it's NOT the root "C:/cierres de caja/"
        if sys.platform == 'win32':
             self.assertNotEqual(path, "C:/cierres de caja/")
             self.assertNotEqual(path, "C:\\cierres de caja\\")

    @patch('iniciarVentaW.os.makedirs')
    @patch('iniciarVentaW.datetime')
    @patch('iniciarVentaW.Workbook')
    @patch('iniciarVentaW.messagebox')
    def test_guardar_execution_path(self, mock_mb, mock_wb, mock_dt, mock_makedirs):
        """Verify the execution flow uses the dynamic path."""
        # Setup
        iniciarVentaW.TURNO_SELECCIONADO = "Turno_Mañana"
        iniciarVentaW.widgets = {}

        # Mock datetime
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-10-27"
        mock_dt.now.return_value = mock_now

        # Run
        iniciarVentaW.guardar_cierre_caja_excel()

        # Verify os.makedirs called
        self.assertTrue(mock_makedirs.called)
        args, _ = mock_makedirs.call_args
        called_path = args[0]

        home = os.path.expanduser("~")
        self.assertTrue(called_path.startswith(home))

if __name__ == '__main__':
    unittest.main()
