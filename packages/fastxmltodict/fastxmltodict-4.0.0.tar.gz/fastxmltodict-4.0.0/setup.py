from setuptools import setup, find_packages, Extension
import shutil
from Cython.Build import cythonize

# Очищаем исходный код и временные файлы
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)


setup(
    name="fastxmltodict",
    version="4.0.0",
    author="MichaelScofield",  # Автор
    description="Быстрый парсер XML в dict",  # Короткое описание
    long_description=open("README.md").read(),  # Длинное описание (из файла README.md)
    packages=find_packages(include=["fastxmltodict", "fastxmltodict.*"]),
    package_data={"fastxmltodict": ["*.so", "*.pyd"]},  # Добавляем бинарные файлы
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# python setup.py sdist bdist_wheel
# twine upload dist/*