"""
معالج الترجمة بالذكاء الاصطناعي
AI Translation module
"""

import logging
from typing import List, Optional, Dict
import numpy as np

logger = logging.getLogger(__name__)


class AITranslator:
    """
    فئة الترجمة بالذكاء الاصطناعي
    Class for AI-powered translation
    """
    
    def __init__(self, source_lang: str = 'en', target_lang: str = 'ar'):
        """
        تهيئة المترجم
        Initialize translator
        
        Args:
            source_lang: اللغة المصدر (الإنجليزية)
            target_lang: اللغة الهدف (العربية)
        """
        logger.info(f"تهيئة المترجم من {source_lang} إلى {target_lang}...")
        
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.model = None
        self.tokenizer = None
        
        # تحميل نموذج الترجمة
        self._load_translation_model()
    
    def _load_translation_model(self):
        """
        تحميل نموذج الترجمة
        Load translation model
        """
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            # استخدام نموذج M2M100 للترجمة
            model_name = "facebook/m2m100_418M"
            logger.info(f"جاري تحميل النموذج: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            logger.info("تم تحميل نموذج الترجمة بنجاح")
            
        except ImportError:
            logger.warning("لم يتم تثبيت مكتبة transformers - تحتاج إلى تثبيتها")
            self.model = None
            self.tokenizer = None
        except Exception as e:
            logger.error(f"خطأ في تحميل نموذج الترجمة: {str(e)}")
            self.model = None
            self.tokenizer = None
    
    def translate_text(self, text: str) -> Optional[str]:
        """
        ترجمة نص واحد
        Translate a single text
        
        Args:
            text: النص المراد ترجمته
            
        Returns:
            النص المترجم أو None
        """
        try:
            if self.model is None or self.tokenizer is None:
                logger.error("نموذج الترجمة غير محمل")
                return None
            
            if not text or len(text.strip()) == 0:
                logger.warning("النص فارغ")
                return text
            
            logger.info(f"جاري ترجمة: {text[:50]}...")
            
            # تعيين اللغة المصدر
            self.tokenizer.src_lang = "en"
            
            # ترميز النص
            encoded = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
            
            # إنشاء معرف اللغة الهدف
            target_lang_id = self.tokenizer.convert_tokens_to_ids("ar")
            
            # الترجمة
            generated_tokens = self.model.generate(
                **encoded,
                forced_bos_token_id=target_lang_id,
                max_length=512
            )
            
            # فك ترميز النص المترجم
            translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            
            logger.info(f"تم الترجمة: {translated_text}")
            return translated_text
            
        except Exception as e:
            logger.error(f"خطأ في ترجمة النص: {str(e)}")
            return text
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """
        ترجمة مجموعة من النصوص
        Translate batch of texts
        
        Args:
            texts: قائمة النصوص المراد ترجمتها
            
        Returns:
            قائمة النصوص المترجمة
        """
        try:
            logger.info(f"جاري ترجمة {len(texts)} نصوص...")
            
            translated_texts = []
            for i, text in enumerate(texts):
                translated = self.translate_text(text)
                translated_texts.append(translated if translated else text)
                
                # ط**

