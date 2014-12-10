parserator
==========

Want a domain-specific parser that learns to parse strings probabilistically? Here's a tool that will help you make one! All you need is some training data to teach the parser about its domain.

### What a parser can do
Given a string, a parser will break it out into labeled components. The parser uses conditional random fields to label components based on (1) features of the component string and (2) the order of labels.

A neat thing about a probabilistic approach (as opposed to a rule-based approach) is that the parser can continually learn from new training data, and continually improve its performance.

Here's an example of an [address parser](https://github.com/datamade/usaddress) and a [name parser](https://github.com/datamade/name-parser).

### How to make a parser using parserator
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
    * For examples of features in other domains, see [features for names](https://github.com/datamade/name-parser/blob/master/name_parser/__init__.py#L80-L169) and [features for U.S. addresses](https://github.com/datamade/usaddress/blob/master/usaddress/__init__.py#L48-L112).
4. **Prepare training data**
    * Parserator reads training data in the following XML form, where token text is wrapped in tags representing the correct label, and sequences of tokens are wrapped in a parent label (specified by PARENT\_LABEL in \_\_init\_\_.py):  
    ```
      <Collection>  
        <TokenSequence><label>token</label> <label>token</label> <label>token</label></TokenSequence>  
        <TokenSequence><label>token</label> <label>token</label></TokenSequence>  
        <TokenSequence><label>token</label> <label>token</label> <label>token</label></TokenSequence>  
      </Collection>
    ```
    * If you have labeled strings in other formats, they will need to be converted to this XML format for parserator to read the data. In data\_prep\_utils.py, there are some tools that can help you do this. For example, the sequence2XML function reads labeled sequences represented as a list of tuples and returns the analogous XML represention: ```[(token, label), (token, label), ...]``` -> ```<TokenSequence><label>token</label> <label>token</label> ... </TokenSequence>```
    * If you only have raw, unlabeled strings, parserator can help you manually label tokens through a command line interface. To start a manual labeling task, run ```parserator label [parser module name] --infile [raw data filepath] --outfile [output filepath]```
      - The infile option should be the filepath for a csv, where each line is a string
      - The outfile option should be the filepath for an xml file, where manually labeled training data will be written. If you specify an existing xml file as the outfile, the newly labeled strings will be appended at the end of the xml file.
      - When you exit a manual labeling task, any strings from the infile that were not labeled will be written to a separate csv, with 'unlabeled_' prepended to the filename, so that in the future, you can pick up where you left off.
      - Within the manual labeling task, you will be prompted with tokens to label. To label tokens, enter the number corresponding to the correct tag. To see a mapping of numbers to labels, type 'help'
      - If the parser model (learned_settings.crfsuite by default) already exists, the console labeler will use it to inform the manual labeling task.
      
5. **Train your parser**
    * To train your parser on your labeled training data, run ```parserator train [parser module name] --traindata [training data filepath]```
    * To train the parser on more than one training training data file, separate the filepaths with a comma (no space)
    * After training, your parser will have an updated model, in the form of a .crfsuite settings file (learned_settings.crfsuite by default)
    * Once the settings file exists, the parse and tag methods use it to label tokens in new strings
6. **Repeat steps 3-5 as needed!**
