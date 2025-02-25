from pathlib import Path

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nlpclean',
    version='1.3.0',
    description='Utilities for cleaning up text corpus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shkarupa-alex/nlpclean',
    author='Shkarupa Alex',
    author_email='shkarupa.alex@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=Path("requirements.txt").read_text().splitlines(),
    python_requires='>=3.7.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
