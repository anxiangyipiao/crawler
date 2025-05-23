# 打包src

from setuptools import setup, find_packages


setup(
    name='scrapyProjectSrc',
    version='1.0.0', # Reset version or update as appropriate
    description='Refactored Scrapy project.',
    author='EastonLee',
    author_email='appelapp2017@outlook.com',
    packages=find_packages(where='src'),  # Ensure it finds packages under src
    package_dir={'': 'src'},  # Specify that packages are in src
    install_requires=[
        'fake_useragent',
        'playwright',
        'redis',
        'ddddocr',
        'requests',
        'PyPDF2',
        'redisbloom' # Added based on the new bloom_filter.py
    ],
    entry_points={'scrapy': ['settings = config.settings']},
)
