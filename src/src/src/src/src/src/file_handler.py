"""
معالج الملفات والأرشيفات
File and archive handler module
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """
    فئة معالجة الملفات والأرشيفات
    Class for handling files and archives
    """
    
    def __init__(self):
        """تهيئة معالج الملفات"""
        logger.info("تهيئة معالج الملفات...")
        
        self.supported_archives = ['.7z', '.zip', '.rar']
        self.supported_images = ['.png', '.jpg', '.jpeg']
        self.supported_documents = ['.pdf']
    
    def extract_archive(self, archive_path: str, extract_to: str) -> bool:
        """
        استخراج ملف مضغوط
        Extract compressed archive
        
        Args:
            archive_path: مسار الملف المضغوط
            extract_to: المجلد الهدف للاستخراج
            
        Returns:
            True إذا نجح الاستخراج
        """
        try:
            archive_path = Path(archive_path)
            extract_to = Path(extract_to)
            
            if not archive_path.exists():
                logger.error(f"الملف المضغوط غير موجود: {archive_path}")
                return False
            
            # إنشاء مجلد الاستخراج إذا لم يكن موجوداً
            extract_to.mkdir(parents=True, exist_ok=True)
            
            file_ext = archive_path.suffix.lower()
            
            logger.info(f"جاري استخراج الملف: {archive_path}")
            
            # استخراج حسب نوع الملف
            if file_ext == '.zip':
                return self._extract_zip(archive_path, extract_to)
            elif file_ext == '.7z':
                return self._extract_7z(archive_path, extract_to)
            elif file_ext == '.rar':
                return self._extract_rar(archive_path, extract_to)
            else:
                logger.error(f"نوع الملف غير مدعوم: {file_ext}")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في استخراج الملف: {str(e)}")
            return False
    
    def _extract_zip(self, archive_path: Path, extract_to: Path) -> bool:
        """
        استخراج ملف ZIP
        Extract ZIP archive
        
        Args:
            archive_path: مسار الملف
            extract_to: مجلد الاستخراج
            
        Returns:
            True إذا نجح
        """
        try:
            import zipfile
            
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            logger.info(f"تم استخراج الملف ZIP بنجاح")
            return True
            
        except ImportError:
            logger.error("مكتبة zipfile غير متاحة")
            return False
        except Exception as e:
            logger.error(f"خطأ في استخراج ZIP: {str(e)}")
            return False
    
    def _extract_7z(self, archive_path: Path, extract_to: Path) -> bool:
        """
        استخراج ملف 7z
        Extract 7z archive
        
        Args:
            archive_path: مسار الملف
            extract_to: مجلد الاستخراج
            
        Returns:
            True إذا نجح
        """
        try:
            import py7zr
            
            with py7zr.SevenZipFile(archive_path, 'r') as archive:
                archive.extractall(path=extract_to)
            
            logger.info(f"تم استخراج الملف 7z بنجاح")
            return True
            
        except ImportError:
            logger.error("مكتبة py7zr غير متاحة")
            return False
        except Exception as e:
            logger.error(f"خطأ في استخراج 7z: {str(e)}")
            return False
    
    def _extract_rar(self, archive_path: Path, extract_to: Path) -> bool:
        """
        استخ��اج ملف RAR
        Extract RAR archive
        
        Args:
            archive_path: مسار الملف
            extract_to: مجلد الاستخراج
            
        Returns:
            True إذا نجح
        """
        try:
            import rarfile
            
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                rar_ref.extractall(extract_to)
            
            logger.info(f"تم استخراج الملف RAR بنجاح")
            return True
            
        except ImportError:
            logger.error("مكتبة rarfile غير متاحة")
            return False
        except Exception as e:
            logger.error(f"خطأ في استخراج RAR: {str(e)}")
            return False
    
    def create_archive(self, folder_path: str, archive_path: str,
                      archive_format: str = '7z') -> bool:
        """
        إنشاء ملف مضغوط
        Create compressed archive
        
        Args:
            folder_path: مسار المجلد المراد ضغطه
            archive_path: مسار الملف المضغوط الجديد
            archive_format: صيغة الضغط (7z, zip)
            
        Returns:
            True إذا نجح
        """
        try:
            folder_path = Path(folder_path)
            archive_path = Path(archive_path)
            
            if not folder_path.exists():
                logger.error(f"المجلد غير موجود: {folder_path}")
                return False
            
            logger.info(f"جاري إنشاء ملف مضغوط: {archive_path}")
            
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            if archive_format.lower() == '7z':
                return self._create_7z_archive(folder_path, archive_path)
            elif archive_format.lower() == 'zip':
                return self._create_zip_archive(folder_path, archive_path)
            else:
                logger.error(f"صيغة غير مدعومة: {archive_format}")
                return False
                
        except Exception as e:
            logger.error(f"خطأ في إنشاء الملف المضغوط: {str(e)}")
            return False
    
    def _create_7z_archive(self, folder_path: Path, archive_path: Path) -> bool:
        """
        إنشاء ملف 7z
        Create 7z archive
        
        Args:
            folder_path: مسار المجلد
            archive_path: مسار الملف الجديد
            
        Returns:
            True إذا نجح
        """
        try:
            import py7zr
            
            with py7zr.SevenZipFile(archive_path, 'w') as archive:
                archive.writeall(folder_path, arcname='.')
            
            logger.info(f"تم إنشاء ملف 7z بنجاح")
            return True
            
        except ImportError:
            logger.error("مكتبة py7zr غير متاحة")
            return False
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملف 7z: {str(e)}")
            return False
    
    def _create_zip_archive(self, folder_path: Path, archive_path: Path) -> bool:
        """
        إنشاء ملف ZIP
        Create ZIP archive
        
        Args:
            folder_path: مسار المجلد
            archive_path: مسار الملف الجديد
            
        Returns:
            True إذا نجح
        """
        try:
            import zipfile
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(folder_path.parent)
                        zipf.write(file_path, arcname)
            
            logger.info(f"تم إنشاء ملف ZIP بنجاح")
            return True
            
        except ImportError:
            logger.error("مكتبة zipfile غير متاحة")
            return False
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملف ZIP: {str(e)}")
            return False
    
    def get_files_from_folder(self, folder_path: str,
                             file_extensions: Optional[List[str]] = None) -> List[Path]:
        """
        الحصول على جميع الملفات من مجلد
        Get all files from folder
        
        Args:
            folder_path: مسار المجلد
            file_extensions: قائمة الصيغ المطلوبة (مثل ['.png', '.jpg'])
            
        Returns:
            قائمة الملفات
        """
        try:
            folder_path = Path(folder_path)
            
            if not folder_path.exists():
                logger.error(f"المجلد غير موجود: {folder_path}")
                return []
            
            files = []
            
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    if file_extensions is None or file_path.suffix.lower() in file_extensions:
                        files.append(file_path)
            
            logger.info(f"وجدت {len(files)} ملف في المجلد")
            return files
            
        except Exception as e:
            logger.error(f"خطأ في قراءة المجلد: {str(e)}")
            return []
    
    def copy_file(self, source: str, destination: str) -> bool:
        """
        نسخ ملف
        Copy file
        
        Args:
            source: مسار الملف المصدر
            destination: مسار الملف الهدف
            
        Returns:
            True إذا نجح
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"الملف المصدر غير موجود: {source}")
                return False
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            
            logger.info(f"تم نسخ الملف: {source} -> {destination}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في نسخ الملف: {str(e)}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """
        حذف ملف
        Delete file
        
        Args:
            file_path: مسار الملف
            
        Returns:
            True إذا نجح
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"الملف غير موجود: {file_path}")
                return False
            
            file_path.unlink()
            logger.info(f"تم حذف الملف: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في حذف الملف: {str(e)}")
            return False
    
    def delete_folder(self, folder_path: str) -> bool:
        """
        حذف مجلد
        Delete folder
        
        Args:
            folder_path: مسار المجلد
            
        Returns:
            True إذا نجح
        """
        try:
            folder_path = Path(folder_path)
            
            if not folder_path.exists():
                logger.error(f"المجلد غير موجود: {folder_path}")
                return False
            
            shutil.rmtree(folder_path)
            logger.info(f"تم حذف المجلد: {folder_path}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في حذف المجلد: {str(e)}")
            return False
    
    def get_file_size(self, file_path: str) -> int:
        """
        الحصول على حجم الملف
        Get file size in bytes
        
        Args:
            file_path: مسار الملف
            
        Returns:
            حجم الملف بالبايت
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"الملف غير موجود: {file_path}")
                return 0
            
            return file_path.stat().st_size
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على حجم الملف: {str(e)}")
            return 0
