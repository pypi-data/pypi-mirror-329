import json
import os
import logging
from elog_cli.oauth_login import OAuthDeviceCodeFlow
from elog_cli.token_login import TokenLogin

# Define OAuth2 endpoints and client details
CODE_FLOW_SERVER_URL = os.environ.get("ELOG_CLI_CODE_FLOW_SERVER_URL")
TOKEN_URL = os.environ.get("ELOG_CLI_TOKEN_URL")
CLIENT_ID = os.environ.get("ELOG_CLI_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ELOG_CLI_CLIENT_SECRET")
ENDPOINT_URL = os.environ.get("ELOG_CLI_ENPOINT_URL")
ENDPOINT_URL_PRODUCTION = os.environ.get("ELOG_CLI_ENPOINT_URL_PRODUCTION")
class AuthManager:
    endpoint_url_slected = None
    logger = logging.getLogger(__name__)
    def __init__(self, token_file=".elog_cli/token_data.json"):
        self.client = None
        self.token_file = os.path.join(os.path.expanduser("~"), token_file)
        self.token_data = self.load_token_data()
        self.token_type = self.token_data.get("login_type") if self.token_data else None

        if self.token_type == "oauth":
            self.auth_flow = OAuthDeviceCodeFlow(CLIENT_ID, CLIENT_SECRET, CODE_FLOW_SERVER_URL, TOKEN_URL)
        elif self.token_type == "token":
            self.auth_flow = TokenLogin()
        else:
            self.auth_flow = None

    def set_environment(self, production:bool):
        if production:
            if ENDPOINT_URL_PRODUCTION is None:
                raise ValueError("No production endpoint URL specified.")
            self.endpoint_url_slected = ENDPOINT_URL_PRODUCTION
        else:
            if ENDPOINT_URL is None:
                raise ValueError("No endpoint URL specified.")
            self.endpoint_url_slected = ENDPOINT_URL

    def get_environment_endpoint(self):
        return self.endpoint_url_slected

    def load_token_data(self):
        """Load token data from disk."""
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                return json.load(file)
        return None

    def save_token_data(self, token_data):
        """Save token data to disk."""
        self.token_data = token_data
        self.token_data["login_type"] = self.token_type  # Add login type to token data
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, "w") as file:
            json.dump(self.token_data, file)

    def get_authenticator(self, login_type=None):
        """Perform the login flow based on the token type."""
        if not self.auth_flow or login_type:
            self.token_type = login_type
            if self.token_type == "oauth":
                self.auth_flow = OAuthDeviceCodeFlow(CLIENT_ID, CLIENT_SECRET, CODE_FLOW_SERVER_URL, TOKEN_URL)
            elif self.token_type == "token":
                self.auth_flow = TokenLogin()
            else:
                raise ValueError("Invalid login type specified")
        return self.auth_flow

    def authenticate(self):
        """Authenticate and manage the token data."""
        if self.auth_flow is None:
            raise ValueError("No auth flow set.")
        if not self.token_data:
            self.token_data = self.auth_flow.login(self)
        else:
            tmp_token = self.auth_flow.check_and_refresh_token(self.token_data)
            if tmp_token != self.token_data:
                self.save_token_data(tmp_token)

    def get_access_token(self):
        """Get the current access token."""
        self.authenticate()
        return self.token_data["access_token"]

    def save_token(self, token_data):
        """Save token data to disk."""
        self.token_data = token_data
        self.token_data["login_type"] = self.token_type  # Ensure login type is in token data
        self.save_token_data()
