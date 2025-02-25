from setuptools import setup, Extension  # Импорт инструментов для сборки
from Cython.Build import cythonize  # Импорт функции для компиляции Cython-кода

# Определяем Cython-расширение (компилируемый файл)
ext_modules = [
    Extension("fastxmltodict.core", ["fastxmltodict/core.py"])
]

# Конфигурация пакета
setup(
    name="fastxmltodict",  # Имя пакета
    version="0.1.0",  # Версия
    author="Твое Имя",  # Автор
    author_email="email@example.com",  # Email автора
    description="Быстрый парсер XML в dict на Cython",  # Короткое описание
    long_description=open("README.md").read(),  # Длинное описание (из файла README.md)
    long_description_content_type="text/markdown",
    url="https://github.com/username/fastxmltodict",  # Ссылка на GitHub
    packages=["fastxmltodict"],  # Указываем, какие пакеты включить
    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),  # Компиляция Cython-кода
    classifiers=[  # Категории PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Минимальная версия Python
)
