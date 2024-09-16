import unittest
from datetime import datetime
from unittest.mock import patch

from src import AccountNotFound, MullvadCLI


class TestMullvadCLI(unittest.TestCase):
    """."""

    @patch('src.cli.popen')
    def test_initialization(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Connected to Mullvad"
        cli = MullvadCLI()
        self.assertTrue(cli.is_connected)
        mock_popen.assert_called_with("mullvad status")

    @patch('src.cli.popen')
    def test_version(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Mullvad 2024.1.0"
        cli = MullvadCLI()
        version = cli.version()
        self.assertEqual(version.strip(), "Mullvad 2024.1.0")
        mock_popen.assert_called_with("mullvad -V")

    @patch('src.cli.popen')
    def test_status(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Connected"
        cli = MullvadCLI()
        cli.status()
        self.assertTrue(cli.is_connected)
        mock_popen.assert_called_with("mullvad status")

    @patch('src.cli.popen')
    def test_account_info(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = (
            "Mullvad account: 12345\n"
            "Expires at: 2024-09-16T12:00:00\n"
            "Device name: MyDevice"
        )
        cli = MullvadCLI()
        info = cli.account_info()
        expected_info = {
            "Mullvad account": "12345",
            "Expires at": datetime.fromisoformat("2024-09-16T12:00:00"),
            "Device name": "MyDevice"
        }
        self.assertEqual(info, expected_info)
        mock_popen.assert_called_with("mullvad account get")

    @patch('src.cli.popen')
    def test_account_info_not_logged_in(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Not logged in"
        cli = MullvadCLI()
        with self.assertRaises(AccountNotFound):
            cli.account_info()
        mock_popen.assert_called_with("mullvad account get")

    @patch('src.cli.popen')
    def test_login(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = 'Mullvad account "12345" set'
        cli = MullvadCLI()
        response = cli.login(12345)
        self.assertEqual(response.strip(), 'Mullvad account "12345" set')
        mock_popen.assert_called_with("mullvad account login 12345")

    @patch('src.cli.popen')
    def test_login_account_not_found(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Error: Account Not Found"
        cli = MullvadCLI()
        with self.assertRaises(AccountNotFound):
            cli.login(12345)
        mock_popen.assert_called_with("mullvad account login 12345")

    @patch('src.cli.popen')
    def test_logout(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Removed device from Mullvad account"
        cli = MullvadCLI()
        response = cli.logout()
        self.assertEqual(response.strip(), "Removed device from Mullvad account")
        mock_popen.assert_called_with("mullvad account logout")

    @patch('src.cli.popen')
    def test_set_auto_connect(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = ""
        cli = MullvadCLI()
        response = cli.set_auto_connect("on")
        self.assertEqual(response.strip(), "Successfully set the auto-connect to: `On`")
        mock_popen.assert_called_with("mullvad auto-connect set on")

    @patch('src.cli.popen')
    def test_get_auto_connect(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Autoconnect: on"
        cli = MullvadCLI()
        status = cli.get_auto_connect()
        self.assertEqual(status.strip(), "Autoconnect: on")
        mock_popen.assert_called_with("mullvad auto-connect get")

    @patch('src.cli.popen')
    def test_set_lockdown_mode(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = ""
        cli = MullvadCLI()
        response = cli.set_lockdown_mode("off")
        self.assertEqual(response.strip(), "Successfully set the lockdown-mode to: `Off`")
        mock_popen.assert_called_with("mullvad lockdown-mode set off")

    @patch('src.cli.popen')
    def test_get_lockdown_mode(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = "Block traffic when the VPN is disconnected: off"
        cli = MullvadCLI()
        status = cli.get_lockdown_mode()
        self.assertEqual(status.strip(), "Block traffic when the VPN is disconnected: off")
        mock_popen.assert_called_with("mullvad lockdown-mode get")

    @patch('src.cli.popen')
    def test_connect(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = ""
        cli = MullvadCLI()
        cli.is_connected = False
        response = cli.connect()
        self.assertTrue(response)
        self.assertTrue(cli.is_connected)
        mock_popen.assert_called_with("mullvad connect")

    @patch('src.cli.popen')
    def test_disconnect(self, mock_popen: any) -> None:
        """."""
        mock_popen.return_value.read.return_value = ""
        cli = MullvadCLI()
        cli.is_connected = True
        response = cli.disconnect()
        self.assertTrue(response)
        self.assertFalse(cli.is_connected)
        mock_popen.assert_called_with("mullvad disconnect")


if __name__ == "__main__":
    unittest.main()
