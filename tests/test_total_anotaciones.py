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

# Import the module under test
try:
    import iniciarVentaW
except ImportError as e:
    raise ImportError(f"Failed to import iniciarVentaW: {e}")

class TestTotalAnotaciones(unittest.TestCase):
    def setUp(self):
        # Reset the global ANOTACIONES_TMP list before each test
        iniciarVentaW.ANOTACIONES_TMP.clear()

    def test_sin_anotaciones(self):
        """Test with an empty ANOTACIONES_TMP list."""
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_anotacion_valida(self):
        """Test with a single valid annotation for the vendor."""
        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "JUAN",
            "monto": 100.0,
            "estado": "PENDIENTE",
            "descripcion": "Test"
        })
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 100.0)

    def test_anotacion_otro_vendedor(self):
        """Test that annotations for other vendors are ignored."""
        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "PEDRO",
            "monto": 100.0,
            "estado": "PENDIENTE",
            "descripcion": "Test"
        })
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_anotacion_estado_ignorado(self):
        """Test that annotations with ignored states are skipped."""
        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "JUAN",
            "monto": 100.0,
            "estado": "IMPACTO_QR",
            "descripcion": "Test"
        })
        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "JUAN",
            "monto": 200.0,
            "estado": iniciarVentaW.ESTADO_QR_IMPACTADO,
            "descripcion": "Test"
        })
        # Both should be ignored
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_sumatoria_multiple(self):
        """Test summing multiple valid annotations."""
        iniciarVentaW.ANOTACIONES_TMP.extend([
            {"vendedor": "JUAN", "monto": 50.5, "estado": "PENDIENTE"},
            {"vendedor": "JUAN", "monto": 20.0, "estado": "PENDIENTE"},
            {"vendedor": "PEDRO", "monto": 100.0, "estado": "PENDIENTE"}, # Should be ignored
            {"vendedor": "JUAN", "monto": 10.0, "estado": "IMPACTO_QR"}   # Should be ignored
        ])
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 70.5)

    def test_nombres_similares_match(self):
        """Test fuzzy matching logic via son_nombres_similares."""
        # "JUAN" should match "JUAN PEREZ" if son_nombres_similares allows it.
        # Based on my reading, son_nombres_similares(excel, db) checks subset.
        # If I ask for "JUAN", and annotation is "JUAN PEREZ", words("JUAN") subset words("JUAN PEREZ") -> True.

        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "JUAN PEREZ",
            "monto": 300.0,
            "estado": "PENDIENTE"
        })
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 300.0)

    def test_monto_como_string(self):
        """Test that string amounts are converted to float."""
        iniciarVentaW.ANOTACIONES_TMP.append({
            "vendedor": "JUAN",
            "monto": "150.50",
            "estado": "PENDIENTE"
        })
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 150.5)

if __name__ == "__main__":
    unittest.main()
