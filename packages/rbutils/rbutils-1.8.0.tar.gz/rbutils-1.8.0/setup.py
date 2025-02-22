#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="rbutils",  # 这里是pip项目发布的名称
    version="1.8.0",  # 版本号，数值大的会优先被pip
    keywords=["pip"],  # 关键字
    description="python 常用的工具",  # 描述
    long_description="Junjie's private utils.",
    license="MIT Licence",  # 许可证

    url="https://github.com/Adenialzz/SongUtils",  # 项目相关文件地址，一般是github项目地址即可
    author="robin",  # 作者
    author_email="robin.seu@foxmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["matplotlib", "numpy"]  # 这个项目依赖的第三方库
)
