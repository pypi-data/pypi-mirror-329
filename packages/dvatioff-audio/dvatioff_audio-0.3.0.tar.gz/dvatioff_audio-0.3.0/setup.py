# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dvatioff-audio",  # 包名，在 PyPI 上必须唯一
    version="0.3.0",  # 版本号
    author="dvatiOFF",
    author_email="dvatioff@gmail.com",
    description="Personal audio utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvatiOFF/python-audio-utils",  # 可选
    packages=find_packages(),  # 自动查找需要打包的模块
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 指定最低 Python 版本
)

# 打包上传步骤：
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
# API TOKEN = pypi-AgEIcHlwaS5vcmcCJGY3ZGE0ODU1LTRiYWQtNGQzZC05N2JlLWZlZWY1YmIyYmNmOAACFlsxLFsiZHZhdGlvZmYtYXVkaW8iXV0AAixbMixbIjQxM2ZmYjhmLWY0MjAtNDlmZS1iNjgyLTU1N2QxNWViZWViYyJdXQAABiB-AjgJq5CSZ2ffVWhbg_Fu-NDlHkVLraZ21xDaY5UlGA