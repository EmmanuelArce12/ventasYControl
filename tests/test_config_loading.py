import sys
import os
import configparser
from unittest.mock import MagicMock
import unittest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock dependencies
sys.modules["tkinter"] = MagicMock()
sys.modules["tkinter.filedialog"] = MagicMock()
sys.modules["tkinter.messagebox"] = MagicMock()
sys.modules["tkinter.simpledialog"] = MagicMock()
sys.modules["tkinter.ttk"] = MagicMock()
sys.modules["pyodbc"] = MagicMock()
sys.modules["openpyxl"] = MagicMock()
sys.modules["openpyxl.styles"] = MagicMock()
sys.modules["pandas"] = MagicMock()

import iniciarVentaW

class TestConfigLoading(unittest.TestCase):
    def setUp(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if "DB_IP" in os.environ:
            del os.environ["DB_IP"]

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if "DB_IP" in os.environ:
            del os.environ["DB_IP"]

    def test_defaults(self):
        config = iniciarVentaW.load_db_config()
        self.assertEqual(config["DB_IP"], "192.168.0.100")

    def test_config_file(self):
        with open(self.config_path, "w") as f:
            f.write("[DATABASE]\nDB_IP = 10.10.10.10\n")

        config = iniciarVentaW.load_db_config()
        self.assertEqual(config["DB_IP"], "10.10.10.10")

    def test_env_var(self):
        os.environ["DB_IP"] = "172.16.0.1"
        with open(self.config_path, "w") as f:
            f.write("[DATABASE]\nDB_IP = 10.10.10.10\n")

        config = iniciarVentaW.load_db_config()
        self.assertEqual(config["DB_IP"], "172.16.0.1")

if __name__ == "__main__":
    unittest.main()
