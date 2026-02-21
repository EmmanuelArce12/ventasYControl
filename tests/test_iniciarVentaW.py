
import unittest
from unittest.mock import MagicMock
import sys

# Mocking tkinter and pyodbc to avoid import errors
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()

import iniciarVentaW

class TestTotalAnotaciones(unittest.TestCase):
    def setUp(self):
        # Reset global state
        iniciarVentaW.ANOTACIONES_TMP = []
        iniciarVentaW.ESTADO_QR_IMPACTADO = "IMPACTO_QR"

    def test_empty_annotations(self):
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_no_match(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "PEDRO", "monto": 100.0, "estado": "PENDIENTE"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_single_match(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": 100.0, "estado": "PENDIENTE"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 100.0)

    def test_multiple_matches(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": 100.0, "estado": "PENDIENTE"},
            {"vendedor": "JUAN", "monto": 50.0, "estado": "PENDIENTE"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 150.0)

    def test_ignore_impacto_qr_literal(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": 100.0, "estado": "IMPACTO_QR"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_ignore_impacto_qr_variable(self):
        iniciarVentaW.ESTADO_QR_IMPACTADO = "CUSTOM_STATUS"
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": 100.0, "estado": "CUSTOM_STATUS"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 0.0)

    def test_fuzzy_match(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN PEREZ", "monto": 100.0, "estado": "PENDIENTE"},
        ]
        # "JUAN" matches "JUAN PEREZ" (subset)
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 100.0)

    def test_fuzzy_match_reverse(self):
         iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": 100.0, "estado": "PENDIENTE"},
        ]
         # "JUAN PEREZ" matches "JUAN" (subset)
         self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN PEREZ"), 100.0)

    def test_string_amount(self):
        iniciarVentaW.ANOTACIONES_TMP = [
            {"vendedor": "JUAN", "monto": "100.50", "estado": "PENDIENTE"},
        ]
        self.assertEqual(iniciarVentaW.total_anotaciones_por_vendedor("JUAN"), 100.50)

class TestSonNombresSimilares(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(iniciarVentaW.son_nombres_similares("JUAN", "JUAN"))

    def test_case_insensitive(self):
        self.assertTrue(iniciarVentaW.son_nombres_similares("juan", "JUAN"))

    def test_subset_match(self):
        self.assertTrue(iniciarVentaW.son_nombres_similares("JUAN PEREZ", "JUAN"))
        self.assertTrue(iniciarVentaW.son_nombres_similares("JUAN", "JUAN PEREZ"))

    def test_normalization(self):
        self.assertTrue(iniciarVentaW.son_nombres_similares("1 - JUAN", "JUAN"))
        self.assertTrue(iniciarVentaW.son_nombres_similares("JUAN", "1 - JUAN"))

    def test_roman_velazquez_rule(self):
        # Special rule for Roman Velazquez logic verification
        # The logic prevents partial matching if "ROMAN" is involved but "VELAZQUEZ" is missing in either side.

        # "ROMAN" vs "ROMAN" -> True because db is subset of ex (exact match)
        self.assertTrue(iniciarVentaW.son_nombres_similares("ROMAN", "ROMAN"))

        self.assertTrue(iniciarVentaW.son_nombres_similares("ROMAN VELAZQUEZ", "ROMAN VELAZQUEZ"))

        # ex="ROMAN", db="JUAN ROMAN".
        # pal_db={"JUAN", "ROMAN"}, pal_ex={"ROMAN"}. db NOT subset of ex.
        # "ROMAN" in db -> True. "VELAZQUEZ" missing -> False.
        self.assertFalse(iniciarVentaW.son_nombres_similares("ROMAN", "JUAN ROMAN"))

        # ex="JUAN ROMAN", db="ROMAN".
        # pal_db={"ROMAN"}, pal_ex={"JUAN", "ROMAN"}. db IS subset of ex. -> True.
        self.assertTrue(iniciarVentaW.son_nombres_similares("JUAN ROMAN", "ROMAN"))

    def test_no_match(self):
        self.assertFalse(iniciarVentaW.son_nombres_similares("JUAN", "PEDRO"))

if __name__ == '__main__':
    unittest.main()
