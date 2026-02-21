import unittest
from unittest.mock import MagicMock, patch
import sys
import io
import os

# Add the parent directory (root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

class TestSecurityFix(unittest.TestCase):
    def test_obtener_fecha_internet_uses_https(self):
        with patch('urllib.request.Request') as mock_request:
            with patch('urllib.request.urlopen') as mock_urlopen:
                # Mock the response context manager
                mock_response = MagicMock()
                mock_response.headers = {'Date': 'Thu, 19 Feb 2026 16:00:00 GMT'}

                # Mock the return value of urlopen()
                mock_urlopen.return_value.__enter__.return_value = mock_response

                iniciarVentaW.obtener_fecha_internet()

                # Verify that Request was called with HTTPS
                # Check call args of Request constructor
                self.assertTrue(mock_request.called, "urllib.request.Request was not called")
                args, _ = mock_request.call_args
                if not args:
                    # Could be kwargs
                    kwargs = mock_request.call_args[1]
                    url = kwargs.get('url', '')
                else:
                    url = args[0]

                self.assertTrue(url.startswith("https://"), f"VULNERABILITY DETECTED: URL '{url}' uses insecure HTTP instead of HTTPS")

if __name__ == '__main__':
    unittest.main()
