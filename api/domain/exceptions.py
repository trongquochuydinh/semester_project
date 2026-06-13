class DomainError(Exception):
    """Base class for framework-independent business errors."""


class ValidationError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


class ConflictError(DomainError):
    pass
