from setuptools import setup, find_packages

setup(
    name='esbot',
    version='2.5',                    # إصدار المكتبة
    description='Easy Telegram Bot ',  # وصف مختصر
    author='Saoud',                      # اسم المؤلف
    author_email='ahmedsaoud0037@gmail.com',   # بريدك الإلكتروني
    url='https://t.me/xr_xr4',  # رابط المشروع أو المستودع
    packages=find_packages(),           # لتضمين كل الحزم الموجودة
    install_requires=[                  # المكتبات المطلوبة
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # أو الرخصة التي تختارها
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',            # نسخة البايثون المطلوبة
)
