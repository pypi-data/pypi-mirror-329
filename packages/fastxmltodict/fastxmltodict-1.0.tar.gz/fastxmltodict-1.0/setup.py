from setuptools import setup, find_packages

setup(
    name="fastxmltodict",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests"],
    include_package_data=True,
    description="Модуль с проверкой лицензии",
    author="Ваше имя",
    url="https://github.com/ваш_профиль/mymodule",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
