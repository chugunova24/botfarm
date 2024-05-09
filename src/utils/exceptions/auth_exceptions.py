from src.core.constants import ErrorCode
from src.core.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class InvalidUserUUID(BadRequest):
    DETAIL = ErrorCode.USER_NOT_EXISTS


class LoginTaken(BadRequest):
    DETAIL = ErrorCode.LOGIN_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID
