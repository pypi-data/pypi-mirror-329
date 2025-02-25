from setuptools import setup, find_packages
from pathlib import Path

# خواندن محتوای فایل README
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="aioengine-python",  # تغییر نام بسته
    version="0.0.2",  # نسخه بسته
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "rich",
        "pydantic"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",  # نوع محتوا به فرمت Markdown
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)