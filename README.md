parserator
==========

Want a domain-specific parser that learns to parse strings probabilistically? Here's a tool that will help you make one! All you need is some training data to teach the parser about its domain.

### What a parser can do
Given a string, a parser will break it out into labeled components. The parser uses conditional random fields to label components based on (1) features of the component string and (2) the order of labels.

A neat thing about a probabilistic approach (as opposed to a rule-based approach) is that the parser can continually learn from new training data, and continually improve its performance.

Here's an example of an [address parser](https://github.com/datamade/usaddress) and a [name parser](https://github.com/datamade/name-parser).

### How to make a parser
1. Initialize a new parser

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
2. Configure the parser to your domain
    * configure labels  
        - The labels (i.e. the set of possible tags for the tokens) are defined by LABELS in \_\_init\_\_.py
    * configure tokenizer  
        - The tokenize function in \_\_init\_\_.py determines how any given string will be split into a sequence of tokens to be tagged, via a regex pattern object. In defining the regex pattern, it's helpful to consider what characters should split tokens (e.g. should the string 'foo;bar' be one token or two) and if so, how characters should be captured in tokens (e.g. should 'foo;bar' be split into ['foo;', 'bar'] or ['foo', ';bar']  
        - In the tests repo, there is a test file for testing the performance of the tokenize function. You can adapt it to your needs & run the test w/ ```nosetests .``` to ensure that you are splitting strings properly.
    * optional: additional config
        -
3. Define features relevant to your domain
4. Prepare training data
5. Train your parser
6. Repeat steps 3-5 as needed!
