from setuptools import setup, find_packages

setup(
    name="py-troya-connect",
    version="0.1.25",
    packages=find_packages(),
    install_requires=[
        "pywin32>=223",
    ],
    author="Tolga Kurtulus",
    author_email="tolgakurtulus95@gmail.com",
    description="A Python interface for Attachmate Extra Terminal sessions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tolgakurtuluss/py-troya-connect",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
