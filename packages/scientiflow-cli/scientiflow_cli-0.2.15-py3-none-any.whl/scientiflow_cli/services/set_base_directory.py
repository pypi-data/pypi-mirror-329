import os
import json
from scientiflow_cli.services.request_handler import make_auth_request

def set_base_directory() -> None:
    hostname = input("Enter the hostname for this: ")
    current_working_directory: str = os.getcwd()
    # sends a request to the create-server endpoint
    body = {
      "hostname": hostname,
      "base_directory": current_working_directory,
      "description": ""
    }
    make_auth_request(endpoint="/servers/create-or-update-server", method="POST", data=body, error_message="Unable to set base directory!")
    # stores the current working directory in a .config file
    config_path = os.path.expanduser("~/.scientiflow/config")
    current_working_directory = os.getcwd()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as file:
        file.write(json.dumps({"BASE_DIR": current_working_directory}))
    print(f"Successfully set base directory!")
    return
    