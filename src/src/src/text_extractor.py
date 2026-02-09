"""
معالج استخراج النصوص باستخدام OCR
Text extraction module using OCR
"""

import logging
from typing import List, Tuple, Optional, Dict
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class TextExtractor:
    """
    فئة استخراج النصوص من الصور
    Class for extracting text from images
    """
    
    def __init__(self):
        """تهيئة معالج النصوص"""
        logger.info("تهيئة معالج استخراج النصوص...")
        self.language = 'en'  # اللغة الافتراضية
        self.min_confidence = 0.5  # الحد الأدنى للثقة
        
        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang=['en'])
            logger.info("تم تحميل نموذج PaddleOCR بنجاح")
        except ImportError:
            logger.warning("لم يتم تثبيت PaddleOCR - قد تحتاج إلى تثبيته")
            self.ocr = None
    
    def extract_text(self, image: np.ndarray) -> List[Dict]:
        """
        استخراج النصوص من الصورة
        Extract text from image
        
        Args:
            image: صورة نمباي
            
        Returns:
            قائمة بقواميس تحتوي على النصوص والإحداثيات
        """
        try:
            if self.ocr is None:
                logger.error("نموذج OCR غير محمل")
                return []
            
            logger.info("جاري استخراج النصوص من الصورة...")
            
            # تطبيق OCR على الصورة
            results = self.ocr.ocr(image, cls=True)
            
            extracted_texts = []
            
            if results and results[0]:
                for line in results[0]:
                    for word_info in line:
                        bbox, (text, confidence) = word_info
                        
                        # تصفية النصوص ذات الثقة المنخفضة
                        if confidence >= self.min_confidence:
                            extracted_texts.append({
                                'text': text,
                                'confidence': confidence,
                                'bbox': bbox,  # إحداثيات الصندوق
                            })
            
            logger.info(f"تم استخراج {len(extracted_texts)} نص")
            return extracted_texts
            
        except Exception as e:
            logger.error(f"خطأ في استخراج النصوص: {str(e)}")
            return []
    
    def extract_text_from_bubble(self, bubble_image: np.ndarray) -> Optional[str]:
        """
        استخراج النص من فقاع�� واحدة
        Extract text from a single bubble
        
        Args:
            bubble_image: صورة الفقاعة
            
        Returns:
            النص المستخرج أو None
        """
        try:
            if self.ocr is None:
                return None
            
            results = self.ocr.ocr(bubble_image, cls=True)
            
            if results and results[0]:
                full_text = ""
                for line in results[0]:
                    for word_info in line:
                        _, (text, confidence) = word_info
                        if confidence >= self.min_confidence:
                            full_text += text + " "
                
                return full_text.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"خطأ في استخراج النص من الفقاعة: {str(e)}")
            return None
    
    def get_text_bounding_boxes(self, extracted_texts: List[Dict]) -> List[Tuple]:
        """
        الحصول على صناديق الإحاطة للنصوص
        Get bounding boxes for extracted texts
        
        Args:
            extracted_texts: قائمة النصوص المستخرجة
            
        Returns:
            قائمة بالصناديق الإحاطة
        """
        try:
            bboxes = []
            for item in extracted_texts:
                bbox = item.get('bbox')
                if bbox:
                    # تحويل الإحداثيات إلى صيغة قياسية (x, y, w, h)
                    points = np.array(bbox, dtype=np.int32)
                    x, y = points.min(axis=0)
                    w, h = points.max(axis=0) - points.min(axis=0)
                    bboxes.append((x, y, w, h))
            
            return bboxes
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على صناديق الإحاطة: {str(e)}")
            return []
    
    def filter_text_by_language(self, texts: List[Dict], language: str = 'en') -> List[Dict]:
        """
        تصفية النصوص حسب اللغة
        Filter texts by language
        
        Args:
            texts: قائمة النصوص
            language: اللغة المراد التصفية لها
            
        Returns:
            النصوص المصفاة
        """
        try:
            logger.info(f"تصفية النصوص باللغة: {language}")
            
            filtered_texts = []
            for text_item in texts:
                text = text_item.get('text', '')
                
                # تصفية بسيطة بناءً على الأحرف
                if language == 'en':
                    # التحقق من وجود أحرف إنجليزية
                    if any(c.isascii() for c in text):
                        filtered_texts.append(text_item)
                elif language == 'ar':
                    # التحقق من وجود أحرف عربية
                    if any('\u0600' <= c <= '\u06FF' for c in text):
                        filtered_texts.append(text_item)
            
            logger.info(f"تم تصفية {len(filtered_texts)} نص")
            return filtered_texts
            
        except Exception as e:
            logger.error(f"خطأ في تصفية النصوص: {str(e)}")
            return texts
    
    def merge_adjacent_texts(self, texts: List[Dict], 
                            distance_threshold: int = 10) -> List[Dict]:
        """
        دمج النصوص المتجاورة
        Merge adjacent texts
        
        Args:
            texts: قائمة النصوص
            distance_threshold: الحد الأدنى للمسافة بين النصوص
            
        Returns:
            النصوص المدمجة
        """
        try:
            if not texts:
                return texts
            
            logger.info("جاري دمج النصوص المتجاورة...")
            
            merged = []
            current_group = [texts[0]]
            
            for i in range(1, len(texts)):
                # حساب المسافة بين النصوص
                current_bbox = current_group[-1]['bbox']
                next_bbox = texts[i]['bbox']
                
                # مسافة مبسطة
                distance = abs(next_bbox[0][0] - current_bbox[-1][0])
                
                if distance <= distance_threshold:
                    current_group.append(texts[i])
                else:
                    # إنشاء نص مدمج
                    merged_text = ' '.join([t['text'] for t in current_group])
                    merged.append({
                        'text': merged_text,
                        'confidence': np.mean([t['confidence'] for t in current_group]),
                        'bbox': current_group[0]['bbox'],
                    })
                    current_group = [texts[i]]
            
            # إضافة المجموعة الأخيرة
            if current_group:
                merged_text = ' '.join([t['text'] for t in current_group])
                merged.append({
                    'text': merged_text,
                    'confidence': np.mean([t['confidence'] for t in current_group]),
                    'bbox': current_group[0]['bbox'],
                })
            
            logger.info(f"تم دمج {len(texts)} نص إلى {len(merged)} نص")
            return merged
            
        except Exception as e:
            logger.error(f"خطأ في دمج النصوص: {str(e)}")
            return texts
    
    def clean_text(self, text: str) -> str:
        """
        تنظيف النص
        Clean text
        
        Args:
            text: النص المراد تنظيفه
            
        Returns:
            النص المنظف
        """
        try:
            # إزالة المسافات الزائدة
            text = ' '.join(text.split())
            
            # إزالة الأحرف الخاصة غير المهمة
            text = text.replace('\x00', '').replace('\n', ' ')
            
            return text
            
        except Exception as e:
            logger.error(f"خطأ في تنظيف النص: {str(e)}")
            return text
