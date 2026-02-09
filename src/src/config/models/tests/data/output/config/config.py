"""
ملف الإعدادات الرئيسي للمشروع
Configuration file for Manga AI Translator
"""

import os
from pathlib import Path

# ========== المسارات الأساسية ==========
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
CONFIG_DIR = BASE_DIR / "config"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# ========== إعدادات المدخلات ==========
# الصيغ المدعومة
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']
SUPPORTED_ARCHIVE_FORMATS = ['.7z', '.zip', '.rar']
SUPPORTED_DOCUMENT_FORMATS = ['.pdf']

# حجم الصور الأقصى
MAX_IMAGE_SIZE = (4096, 4096)
MIN_IMAGE_SIZE = (256, 256)

# ========== إعدادات المعالجة ==========
# معاملات PaddleOCR
PADDLEOCR_CONFIG = {
    'use_angle_cls': True,
    'lang': ['en'],
    'use_gpu': True,
}

# معاملات YOLOv8
YOLO_CONFIG = {
    'model': 'yolov8m.pt',
    'confidence': 0.5,
    'iou': 0.45,
}

# معاملات Detectron2
DETECTRON2_CONFIG = {
    'model_name': 'COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml',
}

# ========== إعدادات الترجمة ==========
# نموذج الترجمة
TRANSLATION_MODEL = 'facebook/m2m100_418M'
SOURCE_LANGUAGE = 'en'  # الإنجليزية
TARGET_LANGUAGE = 'ar'  # العربية

# ========== إعدادات معالجة الصور ==========
# حجم الخط الافتراضي
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT = 'Arial'

# الألوان
TEXT_COLOR = (0, 0, 0)  # أسود
BUBBLE_BORDER_COLOR = (0, 0, 0)  # أسود

# ========== إعدادات المعالجة الدفعية ==========
# عدد الصور التي تتم معالجتها في نفس الوقت
BATCH_SIZE = 10
# عدد العمليات المتوازية
NUM_WORKERS = 4

# ========== إعدادات الإخراج ==========
# صيغ الإخراج المدعومة
OUTPUT_FORMATS = ['png', 'jpg', 'pdf', '7z', 'zip']
# جودة الصور JPEG
JPEG_QUALITY = 95

# ========== إعدادات التسجيل ==========
LOG_LEVEL = 'INFO'
LOG_FILE = BASE_DIR / 'logs' / 'manga_translator.log'

# ========== إعدادات الأداء ==========
USE_GPU = True
DEVICE = 'cuda' if USE_GPU else 'cpu'

# ========== إعدادات أخرى ==========
TIMEOUT = 300  # مهلة زمنية بالثواني
RETRY_ATTEMPTS = 3  # عدد محاولات إعادة المحاولة
