# -*- coding: utf-8 -*-
from io import open
from pathlib import Path

from setuptools import setup, find_packages

# ------------------------------------------------------------------------------- #

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()

# ------------------------------------------------------------------------------- #

about = {}
here = Path(__file__).parent
with (here / "src" / "cloudbypass" / "__version__.py").open(encoding="utf-8") as f:
    exec(f.read(), about)

# ------------------------------------------------------------------------------- #


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages("src", exclude=["test", "test*"]),
    package_dir={"": "src"},
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
        'aiohttp>=3.8.6',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
)

# ------------------------------------------------------------------------------- #
