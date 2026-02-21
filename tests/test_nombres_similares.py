import sys
from unittest import TestCase, main
from unittest.mock import MagicMock

# --- MOCKING DEPENDENCIES ---
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()
sys.modules['openpyxl.workbook'] = MagicMock()

# --- IMPORT MODULE UNDER TEST ---
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from iniciarVentaW import son_nombres_similares, normalizar_texto
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

class TestNombresSimilares(TestCase):

    def test_normalizar_texto(self):
        self.assertEqual(normalizar_texto("Juan"), "JUAN")
        self.assertEqual(normalizar_texto("  juan  "), "JUAN")
        self.assertEqual(normalizar_texto("1 - Juan"), "JUAN")
        self.assertEqual(normalizar_texto("123 - Juan Perez"), "JUAN PEREZ")
        self.assertEqual(normalizar_texto(None), "")
        self.assertEqual(normalizar_texto("nan"), "")

    def test_exact_match(self):
        self.assertTrue(son_nombres_similares("Juan Perez", "Juan Perez"))
        self.assertTrue(son_nombres_similares("JUAN PEREZ", "juan perez"))

    def test_subset_db_in_excel(self):
        # DB is subset of Excel -> True
        self.assertTrue(son_nombres_similares("Juan Perez", "Juan"))
        self.assertTrue(son_nombres_similares("Maria Gonzalez Lopez", "Maria Gonzalez"))

    def test_subset_excel_in_db(self):
        # Excel is subset of DB -> True (via last line of function)
        self.assertTrue(son_nombres_similares("Juan", "Juan Perez"))

    def test_roman_rule_match(self):
        # Both have ROMAN VELAZQUEZ -> True
        self.assertTrue(son_nombres_similares("Roman Velazquez", "Roman Velazquez"))
        self.assertTrue(son_nombres_similares("1 - Roman Velazquez", "Roman Velazquez"))

    def test_roman_rule_fail(self):
        # Excel="Roman", DB="Roman Velazquez".
        # pal_db={"ROMAN", "VELAZQUEZ"}, pal_ex={"ROMAN"}.
        # pal_db subset pal_ex -> False.
        # Roman in ex -> True.
        # Velazquez in ex -> False. -> Returns False.
        self.assertFalse(son_nombres_similares("Roman", "Roman Velazquez"))

        # Excel="Roman Velazquez", DB="Roman Riquelme".
        # pal_db={"ROMAN", "RIQUELME"}, pal_ex={"ROMAN", "VELAZQUEZ"}.
        # Subset -> False.
        # Roman check -> True.
        # Velazquez in DB -> False. -> Returns False.
        self.assertFalse(son_nombres_similares("Roman Velazquez", "Roman Riquelme"))

    def test_roman_rule_subset_db(self):
        # Excel="Roman Velazquez", DB="Roman".
        # pal_db={"ROMAN"}, pal_ex={"ROMAN", "VELAZQUEZ"}.
        # pal_db subset pal_ex -> True.
        # Returns True immediately. Roman check skipped.
        self.assertTrue(son_nombres_similares("Roman Velazquez", "Roman"))

    def test_non_matching(self):
        self.assertFalse(son_nombres_similares("Juan", "Pedro"))
        self.assertFalse(son_nombres_similares("Juan Perez", "Maria Perez"))

    def test_empty_none(self):
        self.assertFalse(son_nombres_similares(None, "Juan"))
        self.assertFalse(son_nombres_similares("Juan", None))
        self.assertFalse(son_nombres_similares("", ""))

if __name__ == '__main__':
    main()
