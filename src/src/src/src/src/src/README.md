# 🎨 تطبيق ترجمة المانجا بالذكاء الاصطناعي
# Manga AI Translator

تطبيق متقدم يستخدم الذكاء الاصطناعي لترجمة وتعديل النصوص في المانجا من الإنجليزية إلى العربية تلقائياً.

An advanced application that uses AI to automatically translate and edit manga text from English to Arabic.

---

## 🌟 المميزات الرئيسية

### Core Features

- ✅ **كشف الفقاعات تلقائياً** - Automatic speech bubble detection
- ✅ **استخراج النصوص** - Text extraction using PaddleOCR
- ✅ **ترجمة ذكية** - AI-powered translation (English → Arabic)
- ✅ **رسم النصوص** - Smart text rendering in bubbles
- ✅ **معالجة الملفات** - Support for images, archives (ZIP, 7Z, RAR), PDF
- ✅ **معالجة دفعية** - Batch processing support
- ✅ **تصحيح التشوهات** - Image correction and enhancement
- ✅ **واجهة سهلة الاستخدام** - User-friendly interface

---

## 📦 المتطلبات

### System Requirements

```
Python 3.8+
CUDA 11.0+ (للمعالجة الأسرع - اختياري)
4GB RAM (الحد الأدنى)
8GB RAM (موصى به)
```

---

## 🚀 التثبيت

### Installation

#### 1️⃣ استنساخ المستودع
```bash
git clone https://github.com/zthzyRs/manga-ai-translator.git
cd manga-ai-translator
```

#### 2️⃣ إنشاء بيئة افتراضية
```bash
python -m venv venv
```

#### 3️⃣ تفعيل البيئة الافتراضية

**على Windows:**
```bash
venv\Scripts\activate
```

**على Linux/Mac:**
```bash
source venv/bin/activate
```

#### 4️⃣ تثبيت المكتبات
```bash
pip install -r requirements.txt
```

---

## 💻 الاستخدام

### Usage

#### الاستخدام الأساسي
```python
from src.main import MangaTranslator

# إنشاء كائن المترجم
translator = MangaTranslator()

# ترجمة صورة واحدة
translator.process_image("path/to/image.png")

# ترجمة مجلد كامل
translator.process_folder("path/to/folder")

# ترجمة ملف مضغوط
translator.process_archive("path/to/archive.zip")
```

#### مثال متقدم
```python
from src.image_processor import ImageProcessor
from src.text_extractor import TextExtractor
from src.translator import AITranslator
from src.text_renderer import TextRenderer

# 1. تحميل الصورة
processor = ImageProcessor()
image = processor.load_image("manga.png")

# 2. كشف الفقاعات
bubbles = processor.detect_bubbles(image)

# 3. استخراج النصوص
extractor = TextExtractor()
extracted_texts = extractor.extract_text(image)

# 4. ترجمة النصوص
translator = AITranslator('en', 'ar')
translated_texts = translator.translate_batch(
    [t['text'] for t in extracted_texts]
)

# 5. رسم النصوص المترجمة
renderer = TextRenderer()
for bubble, translated_text in zip(bubbles, translated_texts):
    image = renderer.render_text_in_bubble(
        image, bubble, translated_text
    )

# 6. حفظ النتيجة
processor.save_image(image, "manga_translated.png")
```

---

## 📁 هيكل المشروع

```
manga-ai-translator/
├── src/
│   ├── __init__.py
│   ├── main.py                 # الملف الرئيسي
│   ├── image_processor.py      # معالجة الصور
│   ├── text_extractor.py       # استخراج النصوص
│   ├── translator.py           # الترجمة الذكية
│   ├── text_renderer.py        # رسم النصوص
│   └── file_handler.py         # معالجة الملفات
├── config/
│   ├── __init__.py
│   └── config.py               # الإعدادات
├── models/
│   └── .gitkeep               # مجلد نماذج AI
├── data/
│   └── .gitkeep               # البيانات المدخلة
├── output/
│   └── .gitkeep               # النتائج المخرجة
├── tests/
│   └── __init__.py
├── requirements.txt            # المكتبات المطلوبة
└── README.md                   # هذا الملف
```

---

## 🔧 الإعدادات

### Configuration

يمكنك تخصيص الإعدادات من خلال ملف `config/config.py`:

```python
# اللغا��
SOURCE_LANGUAGE = 'en'  # الإنجليزية
TARGET_LANGUAGE = 'ar'  # العربية

# حجم الصور
MAX_IMAGE_SIZE = (4096, 4096)
MIN_IMAGE_SIZE = (256, 256)

# معاملات المعالجة
BATCH_SIZE = 10
NUM_WORKERS = 4

# الترجمة
TRANSLATION_MODEL = 'facebook/m2m100_418M'

# الأداء
USE_GPU = True
DEVICE = 'cuda' if USE_GPU else 'cpu'
```

---

## 📊 الأداء

### Performance

| المهمة | الوقت المتوقع |
|------|--------------|
| صورة واحدة (1024x1024) | 5-10 ثواني |
| مجلد 10 صور | 50-100 ثانية |
| ملف ZIP (50 صورة) | 250-500 ثانية |

*الأوقات تقريبية وتعتمد على جهازك*

---

## 🐛 حل المشاكل الشائعة

### Troubleshooting

#### المشكلة: خطأ في تحميل نموذج OCR
```bash
# الحل: تثبيت PaddleOCR يدوياً
pip install paddleocr
```

#### المشكلة: استهلاك عالي للذاكرة
```python
# تقليل حجم الدفعة في config.py
BATCH_SIZE = 5  # بدلاً من 10
```

#### المشكلة: الخطوط العربية لا تظهر بشكل صحيح
```bash
# تثبيت مكتبة pygame
pip install pygame
```

---

## 📝 السجل

### Changelog

#### v1.0.0 (2026-02-09)
- ✅ إطلاق الإصدار الأول
- ✅ دعم الصور والملفات المضغوطة
- ✅ ترجمة ذكية من الإنجليزية للعربية
- ✅ معالجة دفعية

---

## 🤝 المساهمة

### Contributing

نرحب بمساهمتك! يمكنك:

1. Fork المستودع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. كتابة الكود
4. Commit التغييرات (`git commit -m 'Add amazing feature'`)
5. Push إلى الفرع (`git push origin feature/amazing-feature`)
6. فتح Pull Request

---

## 📄 الترخيص

### License

هذا المشروع مرخص تحت رخصة **MIT License** - انظر ملف [LICENSE](LICENSE) للمزيد.

---

## 📧 التواصل

### Contact

- **المؤلف:** zthzyRs
- **البريد الإلكتروني:** [أضف بريدك]
- **GitHub:** [github.com/zthzyRs](https://github.com/zthzyRs)

---

## 🙏 شكر وتقدير

### Acknowledgments

شكراً للمشاريع مفتوحة المصدر التالية:

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Transformers](https://github.com/huggingface/transformers)
- [OpenCV](https://github.com/opencv/opencv)
- [PyTorch](https://github.com/pytorch/pytorch)

---

## ⭐ دعم المشروع

إذا أعجبك هذا المشروع، لا تنسى إضافة نجمة ⭐ للمستودع!

---

**آخر تحديث:** 2026-02-09
