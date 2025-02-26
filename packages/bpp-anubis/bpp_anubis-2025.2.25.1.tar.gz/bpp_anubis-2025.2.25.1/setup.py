import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="bpp-anubis",
    version="2025.2.25.1",
    url="https://gitlab.com/blueprintprep/bpp-qa/utilities/anubis",
    license='MIT',

    author="matthew bahloul",
    author_email="matthew.bahloul@blueprintprep.com",

    description="Tools for running behave tests in parallel",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=[
        'behave==1.2.6',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
            'console_scripts': [
                'anubis = anubis.__main__:main',
            ],
        }
)
