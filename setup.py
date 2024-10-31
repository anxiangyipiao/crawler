# 打包base

from setuptools import setup, find_packages


setup(
    name='baseSpider',
    version='1.0.0',
    description='Base spider needed by all other spiders overfall.',
    author='EastonLee',
    author_email='appelapp2017@outlook.com',
    packages=find_packages(),
    install_requires=[
        'fake_useragent',
        'playwright',
        'mmh3',
        'redis',
        'ddddocr',
        'requests',
    ],
)
