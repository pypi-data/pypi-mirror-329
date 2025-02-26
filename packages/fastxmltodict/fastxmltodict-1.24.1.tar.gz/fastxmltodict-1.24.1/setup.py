from setuptools import setup, find_packages
import shutil

shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)


setup(
    name="fastxmltodict",
    version="1.24.1",
    author="MichaelScofield",
    description = "A fast and lightweight library for converting XML to a Python dictionary.",
    packages=find_packages(include=["fastxmltodict", "fastxmltodict.*"]),
    package_data={"fastxmltodict": ["*.so", "*.pyd"]},
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