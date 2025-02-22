
from click.testing import CliRunner
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import cli

@patch("auth_manager.AuthManager.login")
def test_login(mock_login):
    mock_login.return_value = None  # login does not return anything
    runner = CliRunner()

    result = runner.invoke(cli, ["login"])
    assert result.exit_code == 0
    mock_login.assert_called_once()  # Ensure login was invoked