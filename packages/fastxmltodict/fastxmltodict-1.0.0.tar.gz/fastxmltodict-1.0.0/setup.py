from setuptools import setup, find_packages

setup(
    name="fastxmltodict",
    version="1.0.0",
    packages=find_packages(),
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