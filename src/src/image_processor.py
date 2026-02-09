"""
معالج الصور والفقاعات
Image and bubble processor module
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    فئة معالجة الصور والفقاعات
    Class for processing images and speech bubbles
    """
    
    def __init__(self):
        """تهيئة معالج الصور"""
        logger.info("تهيئة معالج الصور...")
        self.min_bubble_area = 100  # الحد الأدنى لمساحة الفقاعة
        
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        تحميل الصورة
        Load image from file
        
        Args:
            image_path: مسار الصورة
            
        Returns:
            الصورة أو None إذا فشل التحميل
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"فشل تحميل الصورة: {image_path}")
                return None
            logger.info(f"تم تحميل الصورة بنجاح: {image_path}")
            return image
        except Exception as e:
            logger.error(f"خطأ في تحميل الصورة: {str(e)}")
            return None
    
    def detect_bubbles(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        كشف الفقاعات في الصورة
        Detect speech bubbles in the image
        
        Args:
            image: الصورة المدخلة
            
        Returns:
            قائمة بإحداثيات الفقاعات (x, y, w, h)
        """
        try:
            logger.info("جاري كشف الفقاعات...")
            
            # تحويل إلى رمادي
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # تطبيق عتبة ثنائية
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # إيجاد الحدود
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            bubbles = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # تصفية الفقاعات الصغيرة جداً
                if area > self.min_bubble_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    bubbles.append((x, y, w, h))
            
            logger.info(f"تم كشف {len(bubbles)} فقاعة")
            return bubbles
            
        except Exception as e:
            logger.error(f"خطأ في كشف الفقاعات: {str(e)}")
            return []
    
    def extract_bubble_region(self, image: np.ndarray, 
                             bubble: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """
        استخراج منطقة الفقاعة
        Extract bubble region from image
        
        Args:
            image: الصورة الأصلية
            bubble: إحداثيات الفقاعة (x, y, w, h)
            
        Returns:
            صورة الفقاعة المستخرجة
        """
        try:
            x, y, w, h = bubble
            region = image[y:y+h, x:x+w]
            return region
        except Exception as e:
            logger.error(f"خطأ في استخراج منطقة الفقاعة: {str(e)}")
            return None
    
    def correct_distortion(self, image: np.ndarray) -> np.ndarray:
        """
        تصحيح التشوهات البصرية
        Correct visual distortions
        
        Args:
            image: الصورة المدخلة
            
        Returns:
            الصورة المصححة
        """
        try:
            logger.info("جاري تصحيح التشوهات...")
            
            # تطبيق مرشح bilateralFilter لتنعيم الصورة
            corrected = cv2.bilateralFilter(image, 9, 75, 75)
            
            return corrected
            
        except Exception as e:
            logger.error(f"خطأ في تصحيح التشوهات: {str(e)}")
            return image
    
    def remove_background(self, image: np.ndarray) -> np.ndarray:
        """
        إزالة الخلفية حول النص
        Remove background around text
        
        Args:
            image: الصورة المدخلة
            
        Returns:
            الصورة بدون خلفية
        """
        try:
            logger.info("جاري إزالة الخلفية...")
            
            # تطبيق adaptive threshold
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
            
            return result
            
        except Exception as e:
            logger.error(f"خطأ في إزالة الخلفية: {str(e)}")
            return image
    
    def straighten_image(self, image: np.ndarray) -> np.ndarray:
        """
        تصحيح ميل الصورة
        Straighten tilted image
        
        Args:
            image: الصورة المائلة
            
        Returns:
            الصورة المصححة
        """
        try:
            logger.info("جاري تصحيح ميل الصورة...")
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # كشف الخطوط
            lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
            
            if lines is not None and len(lines) > 0:
                angle = 0
                for rho, theta in lines[0]:
                    angle = (theta * 180 / np.pi) - 90
                    if angle < 0:
                        angle += 180
                    break
                
                # تدوير الصورة
                h, w = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(image, M, (w, h))
                
                return rotated
            
            return image
            
        except Exception as e:
            logger.error(f"خطأ في تصحيح الميل: {str(e)}")
            return image
    
    def save_image(self, image: np.ndarray, output_path: str) -> bool:
        """
        حفظ الصورة
        Save image to file
        
        Args:
            image: الصورة المراد حفظها
            output_path: مسار الحفظ
            
        Returns:
            True إذا نجح الحفظ
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(output_path, image)
            logger.info(f"تم حفظ الصورة: {output_path}")
            return True
        except Exception as e:
            logger.error(f"خطأ في حفظ الصورة: {str(e)}")
            return False
    
    def resize_image(self, image: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        تغيير حجم الصورة
        Resize image
        
        Args:
            image: الصورة المدخلة
            width: العرض الجديد
            height: الارتفاع الجديد
            
        Returns:
            الصورة المعاد تحديد حجمها
        """
        try:
            resized = cv2.resize(image, (width, height))
            return resized
        except Exception as e:
            logger.error(f"خطأ في تغيير حجم الصورة: {str(e)}")
            return image
