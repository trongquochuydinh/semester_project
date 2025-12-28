class UserAlreadyLoggedInError(Exception):
    pass

class TokenExpiredError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class AuthError(Exception):
    pass

class InvalidCredentialsError(AuthError):
    pass

class UserDisabledError(AuthError):
    pass
