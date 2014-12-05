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
2. Configure the parser to your domain
    * configure labels
    * configure tokenizer
3. Define features relevant to your domain
4. Prepare training data
5. Train your parser
6. Repeat steps 3-5 as needed!
