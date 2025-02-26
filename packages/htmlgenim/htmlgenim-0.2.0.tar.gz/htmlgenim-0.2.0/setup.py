from setuptools import setup, find_packages

setup(
    name="htmlgenim",
    version="0.2.0",
    author="improve",
    author_email="vlasav227@mail.ru",
    description="Простой генератор HTML-страниц",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)