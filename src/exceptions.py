class DocDigitalesAPIError(Exception):
    """Excepción base para errores de la API de DocDigitales"""
    pass

class AuthenticationError(DocDigitalesAPIError):
    """Excepción para errores de autenticación"""
    pass

class ValidationError(DocDigitalesAPIError):
    """Excepción para errores de validación de datos"""
    pass

class APIError(DocDigitalesAPIError):
    """Excepción para errores generales de la API"""
    pass 