# elog-cli

## Overview

`elog-cli` is a command-line interface for managing elog entries and authentication. It interacts with the elog management backend and supports OAuth2 authentication.

## Installation

To install `elog-cli`, clone the repository and install the required dependencies:

```sh
git clone https://github.com/yourusername/elog-cli.git
cd elog-cli
pip install -r requirements.txt
```

## Environment Variables

The following environment variables need to be set for the authentication manager to work:

- `ELOG_CLI_CODE_FLOW_SERVER_URL`: The URL of the OAuth2 code flow server (e.g., `https://<hostname>/device/code`).
- `ELOG_CLI_TOKEN_URL`: The URL to obtain the token (e.g., `https://<hostname>/token`).
- `ELOG_CLI_CLIENT_ID`: The client ID for OAuth2 authentication.
- `ELOG_CLI_CLIENT_SECRET`: The client secret for OAuth2 authentication.
- `ELOG_CLI_ENPOINT_URL`: The base URL for the elog management backend client.

## Development

This project uses a devcontainer to run a complete setup environment to permit developers to work on the CLI. The devcontainer starts the elog backend container so the developer can interact with the backend without using the official one.

1. Download the mock user authentication data:
    ```sh
    wget http://elog:8080/v1/mock/users-auth -O user.json
    ```

2. Generate the Python client from the OpenAPI specification:
    ```sh
    ~/.local/bin/openapi-python-client generate --url http://elog:8080/api-docs --output-path elog_management_backend_client --overwrite
    ```

3. Ensure all required environment variables are set:
    ```sh
    export ENPOINT_URL="http://elog:8080"
    ```

4. Run the application:
    ```sh
    python main.py login --login-type token
    ```
    and paste one of the tokens found in the above downloaded `user.json`.

## Helper Executable

A helper executable `elog-cli` is provided to simplify running the CLI. This script loads environment variables from a `.env` file and locates the `main.py` script to execute it. elog-cli helper try to find the `.env` file into the same directory of the script, to modify this behaviour the `ELOG_CLI_ENV_FILE_PATH` environment variable that point to the specific `.env` file can be used.

### Usage

1. Ensure the `.env` file is present in the root directory of the project.
2. Make the `elog-cli` script executable:
    ```sh
    chmod +x elog-cli
    ```
3. Run the `elog-cli` script with the desired commands:
    ```sh
    ./elog-cli login --login-type token
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## patching on e;log generated rest api
patch class ```NewEntryWithAttachmentBody``` on file ```elog_cli/elog_management_backend_client/models/new_entry_with_attachment_body.py```
``` python
    def to_multipart(self) -> dict[str, Any]:
        fields = [("entry", (None, json.dumps(self.entry.to_dict()).encode(), "application/json"))]

        # Include files
        if not isinstance(self.files, Unset):
            for files_item_data in self.files:
                # Convert each file to a tuple (fieldname, content, content_type)
                files_item = files_item_data.to_tuple()
                fields.append(("files", (files_item[0], files_item[1], files_item[2])))

        # Add additional properties
        for prop_name, prop in self.additional_properties.items():
            fields.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return fields
```