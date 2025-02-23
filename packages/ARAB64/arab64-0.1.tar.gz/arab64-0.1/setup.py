import setuptools

setuptools.setup(
    name='ARAB64',  # اسم المكتبة
    version='0.1',  # الإصدار
    author='TAN',  # المؤلف
    description='MT FIRST LIB TEST IT',  # وصف قصير للمكتبة
    long_description=open('README.md').read(),  # وصف مفصل (من ملف README)
    long_description_content_type='text/markdown',  # نوع المحتوى لوصف الملف
    packages=setuptools.find_packages(),  # العثور على جميع الحزم في المكتبة
    classifiers=[
        "Programming Language :: Python :: 3",  # دعم لغة Python 3
        "Operating System :: OS Independent",  # دعم أي نظام تشغيل
        "License :: OSI Approved :: MIT License",  # الترخيص (MIT)
    ],
    python_requires='>=3.6',  # الحد الأدنى من إصدار Python
)