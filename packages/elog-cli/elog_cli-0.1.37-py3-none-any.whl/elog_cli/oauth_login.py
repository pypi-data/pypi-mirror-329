import requests
import time
import jwt  # Ensure PyJWT is installed
import click

class OAuthDeviceCodeFlow:
    def __init__(self, client_id, client_secret, auth_server_url, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_server_url = auth_server_url
        self.token_url = token_url

    def get_device_code(self):
        """Request device code from the authorization server."""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "openid profile offline_access email"
        }
        response = requests.post(self.auth_server_url, data=payload)
        response.raise_for_status()
        return response.json()

    def poll_for_token(self, device_code, interval):
        """Poll for token until the user authenticates or timeout."""
        payload = {
            "client_id": self.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }

        while True:
            response = requests.post(self.token_url, data=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error = response.json().get("error")
                if error == "authorization_pending":
                    time.sleep(interval)
                elif error == "slow_down":
                    interval += 5
                    time.sleep(interval)
                else:
                    raise click.ClickException(f"Error: {error}")
            else:
                response.raise_for_status()

    def refresh_token(self, refresh_token):
        """Refresh the access token using the refresh token."""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(self.token_url, data=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise click.ClickException(f"Error refreshing token: {e}")
        return response.json()

    def check_and_refresh_token(self, token_data):
        """Check the JWT validity and refresh it when it is at 80% of the validity."""
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]

        # Decode the JWT without signature verification
        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise click.ClickException("Access token has expired.")
        except jwt.InvalidTokenError:
            raise click.ClickException("error_message: Invalid token.")

        exp = decoded_token["exp"]
        iat = decoded_token["iat"]

        current_time = time.time()
        token_lifetime = exp - iat
        time_elapsed = current_time - iat
        if time_elapsed / token_lifetime >= 0.8:
            print("Refreshing access token...")
            new_token_data = self.refresh_token(refresh_token)
            print("Access token refreshed successfully!")
            return new_token_data
        else:
            return token_data