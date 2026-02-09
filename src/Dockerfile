# مرحلة البناء الأساسية
FROM python:3.10-slim as base

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# تثبيت المتطلبات النظامية
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت المكتبات الأساسية
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# -------------------------------------------
# مرحلة التطوير
FROM base as development

# تثبيت المكتبات الإضافية للتطوير
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# نسخ كل المشروع
COPY . .

# تثبيت المشروع في وضع التطوير
RUN pip install -e .

# تعريض المنفذ
EXPOSE 8000 8888

# الأمر الافتراضي
CMD ["python", "src/main.py"]

# -------------------------------------------
# مرحلة الإنتاج
FROM base as production

# تثبيت المكتبات الإضافية المطلوبة في الإنتاج
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# نسخ المشروع
COPY . .

# تثبيت المشروع
RUN pip install .

# إنشاء مستخدم غير root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# التبديل إلى مستخدم غير root
USER appuser

# تعريض المنفذ
EXPOSE 8000

# التحقق من الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# الأمر الافتراضي
CMD ["python", "src/main.py"]

# -------------------------------------------
# مرحلة الاختبار
FROM development as testing

# نسخ ملفات الاختبار
COPY tests/ tests/
COPY pytest.ini .
COPY tox.ini .

# الأمر الافتراضي - تشغيل الاختبارات
CMD ["pytest", "tests/", "-v", "--cov=src"]

# -------------------------------------------
# مرحلة لي��ت - فحص الكود
FROM development as lint

# نسخ الكود
COPY . .

# الأمر الافتراضي - تشغيل الفحص
CMD ["bash", "-c", "flake8 src/ && black --check src/ && isort --check-only src/"]

# -------------------------------------------
# مرحلة التوثيق
FROM development as docs

# تثبيت متطلبات التوثيق
RUN pip install sphinx sphinx-rtd-theme

# نسخ مجلد التوثيق
COPY docs/ docs/

# تعريض المنفذ
EXPOSE 8000

# الأمر الافتراضي - بناء التوثيق
CMD ["bash", "-c", "cd docs && make html && python -m http.server 8000 --directory _build/html"]
