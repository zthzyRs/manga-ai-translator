"""
نظام السجلات - Logger Module
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from src.config import config


def get_logger(
    name: str = __name__,
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """
    الحصول على كائن Logger مخصص
    
    Args:
        name: اسم Logger
        level: مستوى السجل (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: مسار ملف السجل
    
    Returns:
        Logger: كائن Logger مهيأ
    """
    # استخدام المستوى من البيئة أو المعامل
    log_level = level or config.LOG_LEVEL
    log_file = log_file or config.LOG_FILE

    # إنشاء Logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # تجنب إضافة handlers مكررة
    if logger.hasHandlers():
        return logger

    # صيغة السجل
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # معالج لوحة التحكم (Console Handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # معالج الملف (File Handler)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Logger الافتراضي
logger = get_logger("manga-translator")
