from functools import wraps

from fastapi import HTTPException


def permit_only(commands):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            action = kwargs.get("action", None)
            if action not in commands:
                raise HTTPException(
                    status_code=403,
                    detail=f"The action '{action}' is not permitted. Allowed actions are: {[cmd.name for cmd in commands]}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator