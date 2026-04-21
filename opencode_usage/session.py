import json
import os
from datetime import UTC, datetime
from pathlib import Path


SESSION_PATH = Path(".opencode/session.json")


def load_session() -> tuple[str, str] | None:
    if not SESSION_PATH.exists():
        return None

    try:
        payload = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError, OSError:
        return None

    workspace_id = str(payload.get("workspace_id", "")).strip()
    auth_token = str(payload.get("auth_token", "")).strip()

    if not workspace_id or not auth_token:
        return None

    return workspace_id, auth_token


def save_session(workspace_id: str, auth_token: str) -> None:
    SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "workspace_id": workspace_id,
        "auth_token": auth_token,
        "saved_at": datetime.now(UTC).isoformat(),
    }
    SESSION_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.chmod(SESSION_PATH, 0o600)


def clear_session() -> bool:
    if not SESSION_PATH.exists():
        return False

    SESSION_PATH.unlink()

    try:
        SESSION_PATH.parent.rmdir()
    except OSError:
        pass

    return True
