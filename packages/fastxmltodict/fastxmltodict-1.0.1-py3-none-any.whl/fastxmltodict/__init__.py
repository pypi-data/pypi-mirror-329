# fastxmltodict/__init__.py

try:
    from .secure import generate_secret_code, check_license  # Импортируем скомпилированный модуль
except ImportError:
    from .core import generate_secret_code, check_license  # Фолбэк на обычный Python-код

__all__ = ["generate_secret_code", "check_license"]
