.. parserator documentation master file, created by
   sphinx-quickstart on Tue Jan 20 12:22:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to parserator's documentation!
======================================

Contents:

.. toctree::
   :maxdepth: 2

parserator |release|
================

Parserator is a toolkit for making domain-specific probabilistic parsers, built on python-crfsuite. To create a parser, all you need is some training data to teach your parser about its domain.

Parserator will help you:
* initialize a parser module
* create labeled training data from unlabeled strings
* train your parser model on labeled training data

What a probabilistic parser does
============
A probabilistic parser makes informed guesses about the structure of messy, unstructured text. Given a string, a parser will break it out into labeled components.

Parserator creates parsers that use conditional random fields to label components based on (1) features of the component string and (2) the order of labels. A probabilistic parser learns about features and labels from labeled training data.

Use cases for a probabilistic parser
============

A probabilistic parser is particularly useful for sets of strings that have common structure/patterns, but can deviate from those patterns in ways that are difficult to anticipate with hard coded rules.

For example, in most cases, US addresses start with street number. But there are exceptions: sometimes valid addresses deviate from this pattern (e.g. addresses starting with building name, PO box) and furthermore, addresses in real datasets often include typos & errors. Because there are infinitely many patterns and possible typos to account for, a probabilistic parser is well-suited to parse US addresses.

A neat thing about a probabilistic approach (as opposed to a rule-based approach) is that the parser can continually learn from new training data, and continually improve its performance.

Some examples of existing parsers that use parserator:
* usaddress - Our first probabilistic parser and the basis for the parserator toolkit, it parses any address in the United States. Read our blog post on how it works.
* name-parser - A parser for romanized person names.

Examples of other domains where a probabilistic parser can be useful:
* addresses in another country
* product names/descriptions (e.g. parsing 'Twizzlers Twists, Strawberry, 16-Ounce Bags (Pack of 6)' into brand, item, flavor, weight, etc)
* citations

Installation
============

.. code-block:: bash

   pip install parserator

How to make a parser using parserator
=======

1. Initialize a new parser

.. code-block:: bash

   parserator init [YOUR PARSER NAME]


Important links
===============

* Documentation: http://parserator.rtfd.org/
* Repository: https://github.com/datamade/parserator
* Issues: https://github.com/datamade/parserator/issues
* Distribution: https://pypi.python.org/pypi/parserator

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

