class ApiError(Exception):
    """Базовое исключение для ошибок API."""
    pass


class BadRequestError(ApiError):
    """Исключение для 400 ошибки."""
    pass


class UnauthorizedError(ApiError):
    """Исключение для 401 ошибки."""
    pass
