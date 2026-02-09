"""
البرنامج الرئيسي - Main Application Module
تطبيق ترجمة المانجا بالذكاء الاصطناعي
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.config import config
from src.image_processor import ImageProcessor
from src.logger import get_logger
from src.translator import MangaTranslator


# إنشاء Logger
logger = get_logger(__name__)


class MangaTranslatorApp:
    """فئة التطبيق الرئيسية"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        تهيئة التطبيق
        
        Args:
            config_path: مسار ملف التكوين (اختياري)
        """
        self.config = config
        self.image_processor = ImageProcessor()
        self.translator = MangaTranslator()
        self.output_dir = self.config.OUTPUT_DIR
        
        logger.info("تم تهيئة تطبيق ترجمة المانجا بنجاح")

    def process_image(self, image_path: Path) -> dict:
        """
        معالجة صورة المانجا
        
        Args:
            image_path: مسار الصورة
        
        Returns:
            قاموس يحتوي على نتائج المعالجة
        """
        try:
            logger.info(f"بدء معالجة الصورة: {image_path}")
            
            # التحقق من وجود الملف
            if not image_path.exists():
                logger.error(f"الملف غير موجود: {image_path}")
                raise FileNotFoundError(f"الملف غير موجود: {image_path}")
            
            # معالجة الصورة
            result = self.image_processor.process(image_path)
            
            if result is None:
                logger.warning(f"فشلت معالجة الصورة: {image_path}")
                return {"status": "error", "message": "فشلت معالجة ��لصورة"}
            
            logger.info(f"تمت معالجة الصورة بنجاح: {image_path}")
            return result
            
        except Exception as e:
            logger.error(f"خطأ في معالجة الصورة: {str(e)}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def translate_text(self, text: str, source_lang: str = "ja", target_lang: str = "ar") -> str:
        """
        ترجمة النص
        
        Args:
            text: النص المراد ترجمته
            source_lang: اللغة الأصلية
            target_lang: اللغة المستهدفة
        
        Returns:
            النص المترجم
        """
        try:
            logger.info(f"بدء ترجمة النص من {source_lang} إلى {target_lang}")
            
            # التحقق من النص
            if not text or not text.strip():
                logger.warning("النص فارغ")
                return ""
            
            # ترجمة النص
            translated = self.translator.translate(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang
            )
            
            logger.info("تمت الترجمة بنجاح")
            return translated
            
        except Exception as e:
            logger.error(f"خطأ في الترجمة: {str(e)}", exc_info=True)
            return ""

    def process_manga(self, input_path: Path, output_path: Optional[Path] = None) -> dict:
        """
        معالجة ملف المانجا كاملاً
        
        Args:
            input_path: مسار الملف أو المجلد
            output_path: مسار الحفظ (اختياري)
        
        Returns:
            قاموس يحتوي على نتائج المعالجة
        """
        try:
            logger.info(f"بدء معالجة المانجا: {input_path}")
            
            # التحقق من المسار
            if not input_path.exists():
                logger.error(f"المسار غير موجود: {input_path}")
                raise FileNotFoundError(f"المسار غير موجود: {input_path}")
            
            # تحديد مسار الحفظ
            if output_path is None:
                output_path = self.output_dir / input_path.name
            
            output_path.mkdir(parents=True, exist_ok=True)
            
            # معالجة الصور
            results = []
            
            if input_path.is_file():
                # معالجة ملف واحد
                result = self.process_image(input_path)
                results.append(result)
            else:
                # معالجة مجلد كامل
                image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
                image_files = [
                    f for f in input_path.iterdir()
                    if f.is_file() and f.suffix.lower() in image_extensions
                ]
                
                logger.info(f"وجدت {len(image_files)} صورة")
                
                for image_file in image_files:
                    result = self.process_image(image_file)
                    results.append(result)
            
            logger.info(f"انتهت المعالجة. تم معالجة {len(results)} صورة")
            
            return {
                "status": "success",
                "total_images": len(results),
                "results": results,
                "output_path": str(output_path)
            }
            
        except Exception as e:
            logger.error(f"خطأ في معالجة المانجا: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    def get_stats(self) -> dict:
        """
        الحصول على إحصائيات التطبيق
        
        Returns:
            قاموس يحتوي على الإحصائيات
        """
        try:
            output_files = list(self.output_dir.glob("*"))
            
            return {
                "config": {
                    "device": self.config.DEVICE,
                    "batch_size": self.config.BATCH_SIZE,
                    "source_language": self.config.SOURCE_LANGUAGE,
                    "target_language": self.config.TARGET_LANGUAGE,
                },
                "output_directory": str(self.output_dir),
                "total_output_files": len(output_files),
                "log_level": self.config.LOG_LEVEL,
            }
        except Exception as e:
            logger.error(f"خطأ في الحصول على الإحصائيات: {str(e)}", exc_info=True)
            return {}


def main():
    """الدالة الرئيسية"""
    
    # إعداد parser للأوامر
    parser = argparse.ArgumentParser(
        description="تطبيق ترجمة المانجا بالذكاء الاصطناعي",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python src/main.py -i image.jpg -o output.jpg
  python src/main.py -i manga_folder/
  python src/main.py --stats
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        type=Path,
        help="مسار الصورة أو المجلد المدخل"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="مسار المجلد المخرج"
    )
    parser.add_argument(
        "--source-lang",
        default="ja",
        help="اللغة الأصلية (افتراضي: ja)"
    )
    parser.add_argument(
        "--target-lang",
        default="ar",
        help="اللغة المستهدفة (افتراضي: ar)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="عرض إحصائيات التطبيق"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="تشغيل وضع التصحيح"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Manga AI Translator v1.0.0"
    )
    
    # تحليل الأوامر
    args = parser.parse_args()
    
    # إنشاء التطبيق
    app = MangaTranslatorApp()
    
    # معالجة الأوامر
    if args.debug:
        logger.setLevel("DEBUG")
        logger.info("تم تشغيل وضع التصحيح")
    
    if args.stats:
        stats = app.get_stats()
        logger.info("إحصائيات التطبيق:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        return 0
    
    if args.input:
        result = app.process_manga(args.input, args.output)
        if result["status"] == "success":
            logger.info(f"اكتملت المعالجة بنجاح")
            logger.info(f"العدد الكلي للصور المعالجة: {result['total_images']}")
            logger.info(f"مسار المخرج: {result['output_path']}")
            return 0
        else:
            logger.error(f"فشلت المعالجة: {result['message']}")
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("تم إيقاف التطبيق بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        logger.error(f"خطأ غير متوقع: {str(e)}", exc_info=True)
        sys.exit(1)
