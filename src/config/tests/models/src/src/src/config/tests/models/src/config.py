"""
تكوين التطبيق - Configuration Module
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """فئة التكوين الرئيسية"""

    # تحميل متغيرات البيئة
    load_dotenv()

    # المسارات
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = Path(os.getenv("DATA_PATH", BASE_DIR / "data"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", BASE_DIR / "output"))
    CONFIG_DIR = Path(os.getenv("CONFIG_PATH", BASE_DIR / "config"))
    MODELS_DIR = Path(os.getenv("MODEL_PATH", BASE_DIR / "models"))

    # السجلات
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "app.log"

    # المعالج
    DEVICE = os.getenv("DEVICE", "cpu")  # cpu أو gpu
    NUM_WORKERS = int(os.getenv("NUM_WORKERS", 4))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))

    # النموذج
    MODEL_NAME = os.getenv("MODEL_NAME", "manga-translator-v1")
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.8))

    # الترجمة
    SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", "ja")
    TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "ar")

    # قاعدة البيانات
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # Redis
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

    # الأمان
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

    # الحالة
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"

    @classmethod
    def create_directories(cls) -> None:
        """إنشاء المجلدات المطلوبة"""
        for directory in [cls.DATA_DIR, cls.OUTPUT_DIR, cls.LOG_DIR, cls.MODELS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_config(cls) -> "Config":
        """الحصول على كائن التكوين"""
        cls.create_directories()
        return cls

    def __repr__(self) -> str:
        return f"<Config: {self.MODEL_NAME}>"


# إنشاء التكوين الافتراضي
config = Config.get_config()
