import click
import jwt

class TokenLogin:
    def __init__(self, static_token=None):
        self.static_token = static_token

    def get_device_code(self):
        """Simulate getting a device code."""
        return {"device_code": "static_device_code"}

    def poll_for_token(self, device_code, interval):
        """Simulate polling for token."""
        return {"access_token": self.static_token, "refresh_token": "static_refresh_token"}

    def refresh_token(self, refresh_token):
        """Simulate refreshing the access token."""
        return {"access_token": self.static_token, "refresh_token": "static_refresh_token"}

    def check_and_refresh_token(self, token_data):
        """Check the JWT validity and refresh it when it is at 80% of the validity."""
        # ...existing code...
        return token_data

    def login(self):
        """Ask the user to paste the token and save it in the AuthManager."""
        # Step 1: Ask user to paste the token
        self.static_token = input("Please paste your static token: ")
        
        # Step 2: Check for token validity
        try:
            jwt.decode(self.static_token, options={"verify_signature": False})
        except jwt.InvalidTokenError:
            raise click.ClickException("Invalid token")

        # Step 3: Save the token in AuthManager
        token_data = {"access_token": self.static_token}
        return token_data

