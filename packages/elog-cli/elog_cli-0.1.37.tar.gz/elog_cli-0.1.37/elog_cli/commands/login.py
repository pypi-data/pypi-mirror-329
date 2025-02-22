import click
import jwt
from elog_cli.oauth_login import OAuthDeviceCodeFlow
from elog_cli.token_login import TokenLogin
from elog_cli.auth_manager import AuthManager

@click.command()
@click.option('--login-type', type=click.Choice(['oauth', 'token']), help="Specify the login type.")
@click.pass_context
def login(ctx, login_type):
    """Authenticate using the chosen login type."""
    auth_manager: AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    abstract_flow = auth_manager.get_authenticator(login_type)
    if login_type == "oauth":
        token_data = login_oauth(abstract_flow)
    elif login_type == "token":
        token_data = login_token(abstract_flow)
    else:
        raise ValueError("Invalid login type specified")
    auth_manager.save_token_data(token_data)
    print("Login successful!")

def login_oauth(oauth_flow:OAuthDeviceCodeFlow):
        """Perform the full device code login flow."""
        try:
            # Step 1: Get device code
            print("Requesting device code...")
            device_data = oauth_flow.get_device_code()

            # Generate a direct URL with the user code included
            verification_uri = device_data['verification_uri']
            user_code = device_data['user_code']
            direct_link = f"{verification_uri}?user_code={user_code}"

            print("Please visit the following link to authenticate:")
            print(direct_link)

            # Wait for user input to proceed
            input("Press Enter after you have completed the login on the web URL...")

            # Step 2: Poll for token
            print("Waiting for user authentication...")
            token_data = oauth_flow.poll_for_token(device_data["device_code"], device_data["interval"])
            print("Authentication successful!")
            return token_data
        except Exception as e:
            raise click.ClickException(f"Login failed: {e}")

def login_token(token_flow: TokenLogin):
    """Ask the user to paste the token and save it in the AuthManager."""
    # Step 1: Ask user to paste the token
    static_token = input("Please paste your static token: ")
    
    # Step 2: Check for token validity
    try:
        jwt.decode(static_token, options={"verify_signature": False})
    except jwt.InvalidTokenError:
        raise click.ClickException("Invalid token")

    # Step 3: Save the token in AuthManager
    token_data = {"access_token": static_token}
    return token_data