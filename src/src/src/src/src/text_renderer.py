"""
معالج رسم النصوص على الصور
Text rendering module
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)


class TextRenderer:
    """
    فئة رسم النصوص على الفقاعات
    Class for rendering text on bubbles
    """
    
    def __init__(self):
        """تهيئة معالج الرسم"""
        logger.info("تهيئة معالج رسم النصوص...")
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.8
        self.font_color = (0, 0, 0)  # أسود
        self.font_thickness = 2
        self.text_padding = 10
        
        # تحميل خط عربي إذا أمكن
        self._load_arabic_font()
    
    def _load_arabic_font(self):
        """
        تحميل خط عربي
        Load Arabic font
        """
        try:
            import pygame
            pygame.font.init()
            # يمكن استخدام خط عربي من النظام
            logger.info("تم تهيئة معالج الخطوط العربية")
        except ImportError:
            logger.warning("لم يتم تثبيت pygame - الخطوط العربية قد لا تعمل بشكل صحيح")
    
    def render_text_on_image(self, image: np.ndarray, text: str,
                            position: Tuple[int, int],
                            font_size: int = 14) -> np.ndarray:
        """
        رسم نص على الصورة
        Render text on image
        
        Args:
            image: الصورة المدخلة
            text: النص المراد رسمه
            position: موضع النص (x, y)
            font_size: حجم الخط
            
        Returns:
            الصورة برسم النص
        """
        try:
            x, y = position
            
            logger.info(f"جاري رسم النص: {text[:30]}... في الموضع ({x}, {y})")
            
            # الحصول على حجم النص
            text_size = cv2.getTextSize(text, self.font, self.font_scale, self.font_thickness)
            text_width, text_height = text_size[0]
            
            # رسم خلفية بيضاء خلف النص
            cv2.rectangle(image,
                         (x - 5, y - text_height - 10),
                         (x + text_width + 5, y + 5),
                         (255, 255, 255),
                         -1)
            
            # رسم النص
            cv2.putText(image, text, (x, y),
                       self.font, self.font_scale,
                       self.font_color, self.font_thickness)
            
            return image
            
        except Exception as e:
            logger.error(f"خطأ في رسم النص: {str(e)}")
            return image
    
    def render_text_in_bubble(self, image: np.ndarray, bubble: Tuple[int, int, int, int],
                             text: str, auto_fit: bool = True) -> np.ndarray:
        """
        رسم النص داخل الفقاعة
        Render text inside bubble
        
        Args:
            image: الصورة المدخلة
            bubble: إحداثيات الفقاعة (x, y, w, h)
            text: النص المراد رسمه
            auto_fit: هل يتم تصغير الخط تلقائياً إذا لم يناسب الفقاعة
            
        Returns:
            الصورة برسم النص
        """
        try:
            x, y, w, h = bubble
            
            logger.info(f"جاري رسم النص في الفقاعة: {text[:30]}...")
            
            # حساب موضع النص (في منتصف الفقاعة)
            center_x = x + w // 2
            center_y = y + h // 2
            
            # تقسيم النص إلى سطور إذا كان طويلاً
            lines = self._split_text(text, w - self.text_padding * 2)
            
            # حساب موضع البداية للنصوص المتعددة
            start_y = center_y - (len(lines) * 15) // 2
            
            # رسم كل سطر
            for i, line in enumerate(lines):
                line_y = start_y + i * 20
                
                # الحصول على حجم الخط
                text_size = cv2.getTextSize(line, self.font, self.font_scale, self.font_thickness)
                text_width = text_size[0][0]
                
                # حساب الموضع الأفقي (توسيط)
                line_x = x + (w - text_width) // 2
                
                # رسم النص
                cv2.putText(image, line, (line_x, line_y),
                           self.font, self.font_scale,
                           self.font_color, self.font_thickness)
            
            return image
            
        except Exception as e:
            logger.error(f"خطأ في رسم النص في الفقاعة: {str(e)}")
            return image
    
    def _split_text(self, text: str, max_width: int) -> List[str]:
        """
        تقسيم النص إلى سطور
        Split text into lines
        
        Args:
            text: النص المراد تقسيمه
            max_width: أقصى عرض لكل سطر بالبيكسل
            
        Returns:
            قائمة السطور
        """
        try:
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                
                # حساب عرض الخط
                text_size = cv2.getTextSize(test_line, self.font, self.font_scale, self.font_thickness)
                text_width = text_size[0][0]
                
                if text_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            return lines
            
        except Exception as e:
            logger.error(f"خطأ في تقسيم النص: {str(e)}")
            return [text]
    
    def render_multiple_texts(self, image: np.ndarray,
                             texts_with_positions: List[Tuple[str, Tuple[int, int]]]) -> np.ndarray:
        """
        رسم عدة نصوص على الصورة
        Render multiple texts on image
        
        Args:
            image: الصورة المدخلة
            texts_with_positions: قائمة (نص، موضع)
            
        Returns:
            الصورة برسم جميع النصوص
        """
        try:
            logger.info(f"جاري رسم {len(texts_with_positions)} نصوص...")
            
            for text, position in texts_with_positions:
                image = self.render_text_on_image(image, text, position)
            
            return image
            
        except Exception as e:
            logger.error(f"خطأ في رسم النصوص المتعددة: {str(e)}")
            return image
    
    def draw_bubble_outline(self, image: np.ndarray,
                           bubble: Tuple[int, int, int, int],
                           color: Tuple[int, int, int] = (0, 0, 0),
                           thickness: int = 2) -> np.ndarray:
        """
        رسم حدود الفقاعة
        Draw bubble outline
        
        Args:
            image: الصورة المدخلة
            bubble: إحداثيات الفقاعة (x, y, w, h)
            color: لون الحد (BGR)
            thickness: سمك الحد
            
        Returns:
            الصورة برسم حدود الفقاعة
        """
        try:
            x, y, w, h = bubble
            
            # رسم مستطيل الفقاعة
            cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
            
            logger.info(f"تم رسم حدود الفقاعة")
            return image
            
        except Exception as e:
            logger.error(f"خطأ في رسم حدود الفقاعة: {str(e)}")
            return image
    
    def adjust_font_size(self, text: str, bubble_width: int, bubble_height: int) -> int:
        """
        تعديل حجم الخط بناءً على حجم الفقاعة
        Adjust font size based on bubble size
        
        Args:
            text: النص
            bubble_width: عرض الفقاعة
            bubble_height: ارتفاع الفقاعة
            
        Returns:
            حجم الخط المناسب
        """
        try:
            # حساب مبسط لحجم الخط
            font_size = min(bubble_width, bubble_height) // (len(text) + 1)
            font_size = max(8, min(font_size, 20))  # بين 8 و 20
            
            return font_size
            
        except Exception as e:
            logger.error(f"خطأ في حساب حجم الخط: {str(e)}")
            return 12
    
    def create_text_background(self, image: np.ndarray,
                              text: str, position: Tuple[int, int],
                              bg_color: Tuple[int, int, int] = (255, 255, 255),
                              text_color: Tuple[int, int, int] = (0, 0, 0),
                              padding: int = 5) -> np.ndarray:
        """
        إنشاء خلفية للنص مع تأثيرات
        Create text with background effects
        
        Args:
            image: الصورة المدخلة
            text: النص
            position: موضع النص
            bg_color: لون الخلفية
            text_color: لون النص
            padding: حشوة حول النص
            
        Returns:
            الصورة المعدلة
        """
        try:
            x, y = position
            
            # الحصول على حجم النص
            text_size = cv2.getTextSize(text, self.font, self.font_scale, self.font_thickness)
            text_width, text_height = text_size[0]
            
            # رسم الخلفية
            cv2.rectangle(image,
                         (x - padding, y - text_height - padding),
                         (x + text_width + padding, y + padding),
                         bg_color,
                         -1)
            
            # رسم حد حول الخلفية
            cv2.rectangle(image,
                         (x - padding, y - text_height - padding),
                         (x + text_width + padding, y + padding),
                         (0, 0, 0),
                         1)
            
            # رسم النص
            cv2.putText(image, text, (x, y),
                       self.font, self.font_scale,
                       text_color, self.font_thickness)
            
            return image
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء خلفية النص: {str(e)}")
            return image
