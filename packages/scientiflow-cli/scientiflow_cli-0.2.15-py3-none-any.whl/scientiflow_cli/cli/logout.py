import os
from scientiflow_cli.services.request_handler import make_auth_request

def logout_user():
    response = make_auth_request(endpoint="/auth/logout",method="POST", error_message="Unable to Logout!")
    if response.status_code == 200:
        print("[+] Logout successful!")
        token_file_path = os.path.expanduser("~/.scientiflow/token")
        key_file_path = os.path.expanduser("~/.scientiflow/key")
        os.remove(token_file_path)
        os.remove(key_file_path)
