import unittest
from unittest.mock import MagicMock, patch
from py_troya_connect import ExtraTerminal, ExtraTerminalError

class TestExtraTerminal(unittest.TestCase):
    @patch('win32com.client.Dispatch')
    def setUp(self, mock_dispatch):
        self.mock_session = MagicMock()
        self.mock_screen = MagicMock()
        self.mock_app = MagicMock()
        
        mock_dispatch.return_value = self.mock_app
        self.mock_app.Sessions.Count = 1
        self.mock_app.Sessions.return_value = self.mock_session
        self.mock_session.Screen = self.mock_screen
        
        self.terminal = ExtraTerminal("1")

    def test_format_command(self):
        terminal = ExtraTerminal("1")
        self.assertEqual(terminal.format_command("test"), "test <ENTER>")
        self.assertEqual(terminal.format_command("test{ENTER}"), "test<ENTER>")

    def test_send_command(self):
        self.terminal.send_keys = MagicMock()
        self.terminal.send_command("test")
        self.terminal.send_keys.assert_called_once_with("test <ENTER>")

    def test_read_screen(self):
        self.mock_screen.GetStringEx.return_value = "test" * 480  # 24x80
        result = self.terminal.read_screen()
        self.assertEqual(len(result), 24)  # Should have 24 lines

    def test_wait_for_text(self):
        self.mock_screen.GetStringEx.return_value = "test found" * 480
        result = self.terminal.wait_for_text("found", timeout=1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
