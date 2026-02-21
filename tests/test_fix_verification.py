import unittest
from unittest.mock import MagicMock, patch
import sys
import io

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

class TestSecurityLogging(unittest.TestCase):
    def test_buscar_transaccion_qr_logging_removed(self):
        # Setup test data
        iniciarVentaW.ANOTACIONES_TMP = [
            {"transaccion": "123", "estado": "PENDIENTE"},
            {"transaccion": "456", "estado": "ASIGNADO_MANUAL"}
        ]

        # Mock sys.stdout to capture prints
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            iniciarVentaW.buscar_transaccion_qr("999")
            output = fake_out.getvalue()

        # Verify that sensitive data IS NOT printed (Fix verification)
        self.assertNotIn("BUSCANDO TRANSACCION: 999", output)
        self.assertNotIn("ANOTACIONES:", output)
        self.assertNotIn("123", output)
        self.assertNotIn("456", output)

if __name__ == '__main__':
    unittest.main()
