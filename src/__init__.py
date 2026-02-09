"""
Manga AI Translator - تطبيق ترجمة المانجا بالذكاء الاصطناعي
"""

__version__ = "1.0.0"
__author__ = "zthzyRs"
__description__ = "Manga AI Translator Application"

# استيراد الوحدات الرئيسية
try:
    from src.config import Config
    from src.logger import get_logger
except ImportError:
    pass

__all__ = [
    "Config",
    "get_logger",
]
