import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import 'iniciarVentaW'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies before importing the module
sys.modules['pandas'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['pyodbc'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openpyxl.styles'] = MagicMock()

# Import the module to be tested
try:
    import iniciarVentaW
except ImportError as e:
    print(f"Failed to import iniciarVentaW: {e}")
    iniciarVentaW = None

class TestConfigLoading(unittest.TestCase):

    def setUp(self):
        if iniciarVentaW is None:
            self.fail("Could not import iniciarVentaW")

        self.original_environ = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_environ)

    @patch('iniciarVentaW.configparser.ConfigParser')
    def test_load_from_config_file(self, mock_config_parser):
        """Test loading configuration from config.ini when environment variables are not set."""
        # Ensure environment variables are not set
        keys = ['DB_IP', 'DB_USER', 'DB_PASS', 'DB_NAME']
        for key in keys:
            if key in os.environ: del os.environ[key]

        # Setup mock config parser
        mock_parser_instance = mock_config_parser.return_value
        mock_parser_instance.read.return_value = ['config.ini']
        mock_parser_instance.__contains__.side_effect = lambda key: key == 'DATABASE'

        # Mock getitem to return a dictionary-like object that supports .get()
        # Since ConfigParser sections act like dicts
        mock_section = {
            'DB_IP': '1.2.3.4',
            'DB_USER': 'testuser',
            'DB_PASS': 'testpass',
            'DB_NAME': 'testdb'
        }
        mock_parser_instance.__getitem__.side_effect = lambda key: mock_section if key == 'DATABASE' else {}

        config = iniciarVentaW.load_db_config()

        self.assertEqual(config['DB_IP'], '1.2.3.4')
        self.assertEqual(config['DB_USER'], 'testuser')
        self.assertEqual(config['DB_PASS'], 'testpass')
        self.assertEqual(config['DB_NAME'], 'testdb')

    def test_load_from_env_vars(self):
        """Test loading configuration from environment variables (priority over config file)."""
        os.environ['DB_IP'] = 'env_ip'
        os.environ['DB_USER'] = 'env_user'
        os.environ['DB_PASS'] = 'env_pass'
        os.environ['DB_NAME'] = 'env_db'

        with patch('iniciarVentaW.configparser.ConfigParser') as mock_config_parser:
            mock_parser_instance = mock_config_parser.return_value
            mock_parser_instance.read.return_value = ['config.ini']
            mock_parser_instance.__contains__.return_value = True
            mock_section = {
                'DB_IP': 'file_ip',
                'DB_USER': 'file_user',
                'DB_PASS': 'file_pass',
                'DB_NAME': 'file_db'
            }
            mock_parser_instance.__getitem__.return_value = mock_section

            config = iniciarVentaW.load_db_config()

            self.assertEqual(config['DB_IP'], 'env_ip')
            self.assertEqual(config['DB_USER'], 'env_user')
            self.assertEqual(config['DB_PASS'], 'env_pass')
            self.assertEqual(config['DB_NAME'], 'env_db')

    @patch('iniciarVentaW.configparser.ConfigParser')
    def test_missing_config_returns_empty(self, mock_config_parser):
        """Test behavior when neither env vars nor config file provide values."""
        keys = ['DB_IP', 'DB_USER', 'DB_PASS', 'DB_NAME']
        for key in keys:
            if key in os.environ: del os.environ[key]

        mock_parser_instance = mock_config_parser.return_value
        mock_parser_instance.read.return_value = [] # File not found

        config = iniciarVentaW.load_db_config()

        self.assertEqual(config['DB_IP'], '')
        self.assertEqual(config['DB_USER'], '')
        self.assertEqual(config['DB_PASS'], '')
        self.assertEqual(config['DB_NAME'], '')

if __name__ == '__main__':
    unittest.main()
