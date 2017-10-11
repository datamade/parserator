parserator
==========
A toolkit for making domain-specific probabilistic parsers

[![Build Status](https://travis-ci.org/datamade/parserator.svg?branch=master)](https://travis-ci.org/datamade/parserator)

Do you have domain-specific text data that would be much more useful if you could derive structure from the strings? This toolkit will help you create a custom NLP model that learns from patterns in real data and then uses that knowledge to process new strings automatically. All you need is some training data to teach your parser about its domain.

## What does probabilistic parser do?
Given a string, a probabilistic parser will break it out into labeled components. The parser uses [conditional random fields](http://en.wikipedia.org/wiki/Conditional_random_field) to label components based on (1) features of the component string and (2) the order of labels.

## When is a probabilistic parser useful?
A probabilistic parser is particularly useful for sets of strings that may have common structure/patterns, but which deviate from those patterns in ways that are difficult to anticipate with hard-coded rules.

For example, in most cases, <a href="http://en.wikipedia.org/wiki/Address_(geography)#United_States">addresses in the United States</a> start with a street number. But there are exceptions: sometimes valid U.S. addresses deviate from this pattern (e.g., addresses starting with a building name or a [P.O. box](http://en.wikipedia.org/wiki/Post-office_box)). Furthermore, addresses in real data sets often include typos and other errors. Because there are infinitely many patterns and possible typos to account for, a probabilistic parser is well-suited to parse U.S. addresses.

With a probabilistic (as opposed to a rule-based approach) approach, the parser can continually learn from new training data and thus continually improve its performance!

Some other examples of domains where a probabilistic parser can be useful:
- addresses in other countries with unfamiliar conventions
- product names/descriptions (e.g., parsing phrases like "Twizzlers Twists, Strawberry, 16-Ounce Bags (Pack of 6)" into brand, item, flavor, weight, etc.)
- citations in academic writing

## Examples of parserator

* [usaddress](https://github.com/datamade/usaddress) - Our first probabilistic parser and the basis for the parserator toolkit, it parses any address in the United States. [Read our blog post on how it works](http://datamade.us/blog/parsing-addresses-with-usaddress).
* [probablepeople](https://github.com/datamade/probablepeople) - Parser for romanized person names.

Try out these parsers on our [web interface](http://parserator.datamade.us/)!

## How to make a parser - quick overview
For more details on each step, see the [parserator documentation](http://parserator.rtfd.org/).

1. **Initialize a new parser**

    ```
    pip install parserator
    parserator init [YOUR PARSER NAME]
    python setup.py develop
    ```

2. **Configure the parser to your domain**

    * configure labels (i.e., the set of possible tags for the tokens)
    * configure the tokenizer (i.e., how a raw string will be split into a sequence of tokens to be tagged)

3. **Define features relevant to your domain**
    * define token-level features (e.g., length, casing)
    * define sequence-level features (e.g., whether a token is the first token in the sequence)

4. **Prepare training data**
    * Parserator reads training data in [XML format](http://en.wikipedia.org/wiki/XML)
    * To create XML training data output from unlabeled strings in a [CSV file](http://en.wikipedia.org/wiki/Comma-separated_values), use parserator's command line interface to manually label tokens. It uses values in first column, and it ignores other columns. To start labeling, run ```parserator label [infile] [outfile] [modulename]```
    * For example, ```parserator label unlabeled/rawstrings.csv labeled_xml/labeled.xml usaddress```

5. **Train your parser**
    * To train your parser on your labeled training data, run ```parserator train [traindata] [modulename]```
    * For example, ```parserator train labeled_xml/labeled.xml usaddress``` or ```parserator train "labeled_xml/*.xml" usaddress```
    * After training, your parser will have an updated model, in the form of a .crfsuite settings file

6. **Repeat steps 3-5 as needed!**

## How to use your new parser
Once you are able to create a model from training data, install your custom parser by running `python setup.py develop`.

Then, in a Python shell, you can import your parser and use the ```parse``` and ```tag``` methods to process new strings. For example, to use the probablepeople module:

```
>>> import probablepeople
>>> probablepeople.parse('Mr George "Gob" Bluth II')
[('Mr', 'PrefixMarital'), ('George', 'GivenName'), ('"Gob"', 'Nickname'), ('Bluth', 'Surname'), ('II', 'SuffixGenerational')]
```

## Important Links
* Documentation: http://parserator.rtfd.org/
* Web interface for trying out parsers: http://parserator.datamade.us/
* Blog post: http://datamade.us/blog/parse-name-or-parse-anything-really
* Repository: https://github.com/datamade/parserator
* Issues: https://github.com/datamade/parserator/issues
* Distribution: https://pypi.python.org/pypi/parserator


## Team

* [Forest Gregg](https://github.com/fgregg), DataMade
* [Cathy Deng](https://github.com/cathydeng), DataMade

## Errors and Bugs

If something is not behaving intuitively, it is a bug and should be reported.
Report an [issue](https://github.com/datamade/parserator/issues).

## Patches and Pull Requests
We welcome your ideas! You can make suggestions in the form of [GitHub issues](https://github.com/datamade/parserator/issues) (bug reports, feature requests, general questions), or you can submit a code contribution via a pull request.

How to contribute code:

- Fork the project.
- Make your feature addition or bug fix.
- Send us a pull request with a description of your work! Don't worry if it isn't perfect: think of a PR as a start of a conversation rather than a finished product.

## Copyright and Attribution

Copyright (c) 2016 DataMade. Released under the [MIT License](https://github.com/datamade/parserator/blob/master/LICENSE).
