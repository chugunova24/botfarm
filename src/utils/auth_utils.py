from typing import Any

from src.core.config import settings


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": settings.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": settings.SECURE_COOKIES,
        "domain": settings.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": settings.REFRESH_TOKEN_EXP,
    }
