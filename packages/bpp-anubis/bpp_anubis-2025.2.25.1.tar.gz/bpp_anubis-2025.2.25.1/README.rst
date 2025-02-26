anubis
======

.. image:: https://img.shields.io/pypi/v/anubis.svg
    :target: https://pypi.python.org/pypi/anubis
    :alt: Latest PyPI version


Framework for running bpp qa

Usage
-----

General structure of anubis command

``anubis -d <path to behave-like directory> -e <environments> -c <mcat, lsat> -p <number of processes> -b <browser to use> -it <tags to include in the run> -et <tags to exclude from the run> -r <results destination json> -rt <number of retries for failed scenarios> -a <path to accounts file> -s <section of accounts file to read; usually "course.env"> -of out``

exact parameters vary from project to project.

Installation
------------
``pip install bpp-anubis``

Requirements
^^^^^^^^^^^^
assertpy

auth0-python

beautifulsoup4

behave-html-formatter

configparser

html5lib

lxml

nested_lookup

pandas

pdfkit

requests

selenium

slack_sdk

uuid

clipboard

Compatibility
-------------

Licence
-------
MIT

Authors
-------

`anubis` was written by `matthew bahloul <matthew.bahloul@blueprintprep.com>`_.
