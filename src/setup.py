from setuptools import setup, find_packages
import os

# قراءة محتوى README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# قراءة المتطلبات من requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# المتطلبات الإضافية للتطوير
extras_require = {
    "dev": [
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.12.0",
        "black>=23.12.1",
        "flake8>=6.1.0",
        "isort>=5.13.2",
        "pylint>=3.0.3",
        "mypy>=1.7.1",
    ],
    "docs": [
        "sphinx>=7.2.6",
        "sphinx-rtd-theme>=2.0.0",
        "sphinx-autodoc-typehints>=1.25.2",
        "myst-parser>=2.0.0",
    ],
    "jupyter": [
        "jupyter>=1.0.0",
        "notebook>=7.0.6",
        "jupyterlab>=4.0.9",
    ],
}

# كل الإضافات معاً
extras_require["all"] = sum(extras_require.values(), [])

setup(
    name="manga-ai-translator",
    version="1.0.0",
    author="zthzyRs",
    author_email="your_email@example.com",
    description="تطبيق ترجمة المانجا بالذكاء الاصطناعي - Manga AI Translator Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zthzyRs/manga-ai-translator",
    project_urls={
        "Bug Reports": "https://github.com/zthzyRs/manga-ai-translator/issues",
        "Source": "https://github.com/zthzyRs/manga-ai-translator",
        "Documentation": "https://github.com/zthzyRs/manga-ai-translator/blob/main/README.md",
        "Changelog": "https://github.com/zthzyRs/manga-ai-translator/blob/main/CHANGELOG.md",
    },
    packages=find_packages(where=".", include=["src*", "config*", "tests*"]),
    package_data={
        "src": ["**/*.py", "**/*.json", "**/*.yaml", "**/*.yml"],
        "config": ["*.py", "*.json", "*.yaml", "*.yml"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Office Suites",
        "Natural Language :: English",
        "Natural Language :: Arabic",
        "Natural Language :: Japanese",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "manga-translator=src.main:main",
        ],
    },
    keywords=[
        "manga",
        "translation",
        "ai",
        "machine learning",
        "ocr",
        "bubble detection",
        "image processing",
        "arabic",
        "japanese",
        "english",
        "nlp",
        "deep learning",
    ],
    zip_safe=False,
    options={
        "bdist_wheel": {"universal": False},
    },
)
