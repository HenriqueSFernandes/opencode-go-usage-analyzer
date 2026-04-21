import getpass


def prompt_workspace_id() -> str:
    while True:
        workspace_id = input("Workspace ID: ").strip()
        if workspace_id:
            return workspace_id
        print("Workspace ID cannot be empty.")


def prompt_auth_token() -> str:
    while True:
        auth_token = getpass.getpass("Auth token: ").strip()
        if auth_token:
            return auth_token
        print("Auth token cannot be empty.")
