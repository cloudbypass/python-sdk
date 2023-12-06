# -*- coding: utf-8 -*-
from io import open
from setuptools import setup, find_packages

# ------------------------------------------------------------------------------- #

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()

# with open("requirements.txt", "r", encoding="utf8") as f:
#     requires = f.read()
#     print(requires.splitlines())
# ------------------------------------------------------------------------------- #

setup(
    name='cloudbypass',
    author='howard',
    author_email='437983438@qq.com',
    version='0.0.1',
    packages=find_packages('cloudbypass'),
    package_dir={'': 'cloudbypass'},
    description='Cloudbypass SDK for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=[
        'cloudflare',
        'bypass',
        'turnstile',
        'scraping',
        'cloudbypass',
        'scrapingbypass',
        'waf',
        'captcha',
        'cloudflare-bypass',
        'cloudflare-scraping',
    ],
    install_requires=[
        'requests>=2.28.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.0',
)

# ------------------------------------------------------------------------------- #
