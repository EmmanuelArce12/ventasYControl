import sys
import types
from unittest.mock import MagicMock

# Mock modules that might fail to import or require display
sys.modules['pyodbc'] = MagicMock()
# sys.modules['tkinter'] = MagicMock() # tkinter is installed, but we want to avoid GUI.
# But the script imports it. If we mock it, we must ensure all used attributes exist.
# MagicMock does that.

# However, `from tkinter import ...` might fail if tkinter is not a package in sys.modules?
# Let's mock it fully.
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

import os
import shutil
# Now import the module under test
import iniciarVentaW

def test_ruta_cierre_caja():
    # Expected path
    expected_path = os.path.join(os.path.expanduser("~"), "cierres de caja")

    # Clean up if it exists
    if os.path.exists(expected_path):
        shutil.rmtree(expected_path)

    # Call the function
    actual_path = iniciarVentaW.obtener_ruta_cierre_caja()

    # Assert path is correct
    print(f"Expected: {expected_path}")
    print(f"Actual:   {actual_path}")
    assert actual_path == expected_path, f"Path mismatch! Expected {expected_path}, got {actual_path}"

    # Assert directory exists
    assert os.path.exists(actual_path), "Directory was not created!"

    print("Test passed!")

if __name__ == "__main__":
    test_ruta_cierre_caja()
