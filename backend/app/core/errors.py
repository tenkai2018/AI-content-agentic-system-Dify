from typing import Any, Optional

from fastapi import HTTPException


def raise_api_error(
    *,
    status_code: int,
    code: str,
    message: str,
    task_id: Optional[str] = None,
    step: Optional[str] = None,
    extra: Optional[dict[str, Any]] = None,
) -> None:
    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if task_id:
        payload["error"]["task_id"] = task_id
    if step:
        payload["error"]["step"] = step
    if extra:
        payload["error"]["extra"] = extra

    raise HTTPException(status_code=status_code, detail=payload)
