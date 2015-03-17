parserator
==========
A toolkit for making domain-specific probabilistic parsers

[![Build Status](https://travis-ci.org/datamade/parserator.svg?branch=master)](https://travis-ci.org/datamade/parserator)

Want a domain-specific parser that learns to parse strings probabilistically? Here's a tool that will help you make one! All you need is some training data to teach the parser about its domain.

## What a probabilistic parser does
Given a string, a parser will break it out into labeled components. The parser uses [conditional random fields](http://en.wikipedia.org/wiki/Conditional_random_field) to label components based on (1) features of the component string and (2) the order of labels.

## parserator examples

* [usaddress](https://github.com/datamade/usaddress) - Our first probabilistic parser and the basis for the parserator toolkit, it parses any address in the United States. [Read our blog post on how it works](http://datamade.us/blog/parsing-addresses-with-usaddress/).
* [probablepeople](https://github.com/datamade/probablepeople) - Parser for romanized person names. 

Try out these parsers on our [web interface](http://parserator.datamade.us/)!

## When is a probabalistic parser useful?
A probabilistic parser is particularly useful for sets of strings that have common structure/patterns, but can deviate from those patterns in ways that are difficult to anticipate with hard coded rules.

For example, in most cases, US addresses start with street number. But there are exceptions: sometimes valid addresses deviate from this pattern (e.g. addresses starting with building name, PO box) and furthermore, addresses in real datasets often include typos & errors. Because there are infinitely many patterns and possible typos to account for, a probabilistic parser is well-suited to parse US addresses.

A neat thing about a probabilistic approach (as opposed to a rule-based approach) is that the parser can continually learn from new training data, and continually improve its performance.

Some other examples of domains where a probabilistic parser can be useful:
- addresses in another country
- product names/descriptions (e.g. parsing 'Twizzlers Twists, Strawberry, 16-Ounce Bags (Pack of 6)' into brand, item, flavor, weight, etc)
- citations

## How to make a parser using parserator
1. **Initialize a new parser**

    ```
    pip install parserator  
    parserator init [YOUR PARSER NAME]  
    ```  
    This will initialize a new parser in your current directory. For example, running ```parserator init foo``` will generate the following directories and files:
    * foo/
      - \_\_init\_\_.py
    * foo_data/
      - labeled_xml/
      - unlabeled/
    * setup.py
    * tests/
      - test_tokenizing.py
2. **Configure the parser to your domain**  
    *NOTE: be thoughtful in this step, because the labels & tokenizer determine how your training data is created/read, and thus will be annoying to change after you've already added labeled training data (step 4)*
    * configure labels  
        - The labels (i.e. the set of possible tags for the tokens) are defined by LABELS in \_\_init\_\_.py
    * configure tokenizer  
        - The tokenize function in \_\_init\_\_.py determines how any given string will be split into a sequence of tokens to be tagged, via a regex pattern object. In defining the regex pattern, it's helpful to consider what characters should split tokens (e.g. should the string 'foo;bar' be one token or two) and if so, how characters should be captured in tokens (e.g. should 'foo;bar' be split into ['foo;', 'bar'] or ['foo', ';bar']  
        - In the tests repo, there is a test file for testing the performance of the tokenize function. You can adapt it to your needs & run the test w/ ```nosetests .``` to ensure that you are splitting strings properly.
    * optional: additional config
        - PARENT\_LABEL and GROUP\_LABEL are training data XML tags (see #4 for more info on the training data format). For example, the name parser has PARENT\_LABEL = 'Name' & GROUP\_LABEL = 'NameCollection'
3. **Define features relevant to your domain**
    * In \_\_init\_\_.py, features are defined in the tokens2features and tokenFeatures functions. Given an individual token, tokenFeatures should return features of that token - for example, a length feature and a word shape (casing) feature.
    * Given a sequence of tokens, tokens2features should return all features for the tokens in the sequence, including positional features - for example, the features of previous/next tokens, and features for tokens that start/end a string.
    * For examples of features in other domains, see [features for names](https://github.com/datamade/probablepeople/blob/master/probablepeople/__init__.py#L80-L169) and [features for U.S. addresses](https://github.com/datamade/usaddress/blob/master/usaddress/__init__.py#L48-L112).
4. **Prepare training data**
    * Parserator reads training data in the following XML form, where token text is wrapped in tags representing the correct label, and sequences of tokens are wrapped in a parent label (specified by PARENT\_LABEL in \_\_init\_\_.py):  
    ```
      <Collection>  
        <TokenSequence><label>token</label> <label>token</label> <label>token</label></TokenSequence>  
        <TokenSequence><label>token</label> <label>token</label></TokenSequence>  
        <TokenSequence><label>token</label> <label>token</label> <label>token</label></TokenSequence>  
      </Collection>
    ```
    * If you only have raw, unlabeled strings, parserator can help you manually label tokens through a command line interface. To start a manual labeling task, run ```parserator label [infile] [outfile] [modulename]```
      - The infile option should be the filepath for a csv, where each line is a string
      - The outfile option should be the filepath for an xml file, where manually labeled training data will be written. If you specify an existing xml file as the outfile, the newly labeled strings will be appended at the end of the xml file.
      - When you exit a manual labeling task, any strings from the infile that were not labeled will be written to a separate csv, with 'unlabeled_' prepended to the filename, so that in the future, you can pick up where you left off.
      - Within the manual labeling task, you will be prompted with tokens to label. To label tokens, enter the number corresponding to the correct tag. To see a mapping of numbers to labels, type 'help'
      - If the parser model (learned_settings.crfsuite by default) already exists, the console labeler will use it to inform the manual labeling task.
    * If you have labeled strings in other formats, they will need to be converted to this XML format for parserator to read the data. In data\_prep\_utils.py, there are some tools that can help you do this. For example, the sequence2XML function reads labeled sequences represented as a list of tuples and returns the analogous XML represention: ```[(token, label), (token, label), ...]``` -> ```<TokenSequence><label>token</label> <label>token</label> ... </TokenSequence>```
      
5. **Train your parser**
    * To train your parser on your labeled training data, run ```parserator train [traindata] [modulename]```
    * To train the parser on more than one training training data file, separate the filepaths with a comma (no space)
    * After training, your parser will have an updated model, in the form of a .crfsuite settings file (learned_settings.crfsuite by default)
    * Once the settings file exists, the parse and tag methods use it to label tokens in new strings
6. **Repeat steps 3-5 as needed!**

## How to use your new parser
Once you are able to create a model from training data, install your parser module. Then, you can use the ```parse``` and ```tag``` methods to process new strings. For example, to use the probablepeople module:

```
>>> import probablepeople  
>>> probablepeople.parse('Mr George "Gob" Bluth II')  
[('Mr', 'PrefixMarital'), ('George', 'GivenName'), ('"Gob"', 'Nickname'), ('Bluth', 'Surname'), ('II', 'SuffixGenerational')]
```

## Important Links
* Documentation: http://parserator.rtfd.org/
* Web interface for trying out parsers: http://parserator.datamade.us/
* Blog post: http://datamade.us/blog/parse-name-or-parse-anything-really/
* Repository: https://github.com/datamade/parserator
* Issues: https://github.com/datamade/parserator/issues
* Distribution: https://pypi.python.org/pypi/parserator
