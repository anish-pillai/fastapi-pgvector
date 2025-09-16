from fastapi import HTTPException
from typing import Any, Optional, Dict


class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details or {},
            },
        )