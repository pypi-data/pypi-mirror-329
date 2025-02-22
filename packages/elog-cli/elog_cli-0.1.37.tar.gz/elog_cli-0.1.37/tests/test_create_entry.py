import json
import os

from unittest.mock import patch
from click.testing import CliRunner
from elog_cli.auth_manager import AuthManager
from elog_cli.main import cli


def user_data():
    with open(os.path.join(os.path.dirname(__file__), '../user.json')) as f:
        return json.load(f)['payload']['Name1 Surname1'] 


def test_create_entry():
    runner = CliRunner()
    token = user_data()
    # Mock the get_access_token method to return the token
    with patch.object(AuthManager, 'get_access_token', return_value=token):
        result = runner.invoke(cli, [
            "create-entry",
            "--title", "Test Entry",
            "--text", "This is a test entry.",
            "--logbooks", "mcc",
            "--attachments", os.path.join(os.path.dirname(__file__), 'test.png'),
            "--attachments", os.path.join(os.path.dirname(__file__), 'test.png')
        ])
        
        assert result.exit_code == 0
        assert 'New entry created with id' in result.output

def test_create_entry_supersede():
    runner = CliRunner()
    token = user_data()
    # Mock the get_access_token method to return the token
    with patch.object(AuthManager, 'get_access_token', return_value=token):
        result = runner.invoke(cli, [
            "create-entry",
            "--title", "Test Entry",
            "--text", "This is a test entry.",
            "--logbooks", "mcc",
        ])
        
        assert result.exit_code == 0
        assert 'New entry created with id' in result.output
        #split on ':' and get the last element which is the entry id
        entry_id = result.output.split(':')[-1].strip()

        result_supersede = runner.invoke(cli, [
            "create-entry",
            "--title", "Test Entry",
            "--text", "This is a test entry that supersede another.",
            "--logbooks", "mcc",
            "--supersede-of", str(entry_id)
        ])
        assert result_supersede.exit_code == 0
        assert 'New entry created with id' in result_supersede.output