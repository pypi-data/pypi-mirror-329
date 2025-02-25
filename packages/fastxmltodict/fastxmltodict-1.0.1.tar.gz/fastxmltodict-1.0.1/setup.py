from setuptools import setup, find_packages

setup(
    name="fastxmltodict",
    version="1.0.1",
    author="Your Name",
    author_email="your@email.com",
    description="Защищённый модуль для генерации кодов",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/securemodule",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
