import config
import os
from training import train
import pycrfsuite
import warnings


try :
    TAGGER = pycrfsuite.Tagger()
    path = os.path.split(os.path.abspath(__file__))[0] + '/' + config.MODEL_FILE
    TAGGER.open(path)
except IOError :
    warnings.warn("You must train the model (run training/training.py) and create the "+config.MODEL_FILE+" file before you can use the parse and tag methods")



def parse(raw_string) :

    tokens = tokenize(raw_string)

    if not tokens :
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)


def tag(raw_string) :
    tagged = OrderedDict()
    for token, label in parse(raw_string) :
        tagged.setdefault(label, []).append(token)

    for token in tagged :
        component = ' '.join(tagged[token])
        component = component.strip(" ,;")
        tagged[token] = component

    return tagged


# This defines how a raw string is split into tokens, to be tagged
def tokenize(raw_string) :
    re_tokens = re.compile(r"""
    \(*[^\s,;()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(raw_string)

    if not tokens :
        return []

    return tokens

#####################################################
# This is where sequence-level features are defined # 
# e.g. first token, last token, etc                 #
#####################################################
def tokens2features(tokens):
    
    feature_sequence = [config.tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    seen_comma = False

    for token in tokens[1:] :
        token_features = config.tokenFeatures(token) 

        # # This is an example of a feature for whether a comma has been encountered in previous tokens
        # if not seen_comma and previous_features['comma'] :
        #     seen_comma = True
        # if seen_comma :
        #     token_features['seen.comma'] = True

        current_features = token_features.copy()

        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features        
            
        feature_sequence.append(token_features)

        previous_features = current_features

    if len(feature_sequence) > 1 :
        feature_sequence[0]['rawstring.start'] = True
        feature_sequence[-1]['rawstring.end'] = True
        feature_sequence[1]['previous']['rawstring.start'] = True
        feature_sequence[-2]['next']['rawstring.end'] = True

    else : 
        feature_sequence[0]['singleton'] = True

    return feature_sequence



###########################################################
# This is where features of individual tokens are defined # 
###########################################################

VOWELS_Y = tuple('aeiouy')

def tokenFeatures(token) :

    if token in (u'&') :
        token_chars = token_chars_lc = token
        
    else :
        # this is the token w/o punctuation
        token_chars = re.sub(r'(^[\W]*)|([^\w]*$)', u'', token)
        # this is the token w/o punctuation & w/o capitalization
        token_chars_lc = re.sub(r'\W', u'', token_chars.lower())

    # below are some basic examples of feature definitions
    features = {
        # lowercase chars example
        'nopunc' : token_chars_lc,
        # word shape example
        'case' : casing(token_chars),
        # length example
        'length' : len(token_chars_lc),
        # vowels example
        'has.vowels'  : bool(set(token_chars_lc[1:]) & set('aeiouy')),
        # vowel ratio example
        'more.vowels' : vowelRatio(token_chars_lc)
                }

    reversed_token = token_chars_lc[::-1]
    for i in range(1, len(token_chars_lc)) :
        features['prefix_%s' % i] = token_chars_lc[:i]
        features['suffix_%s' % i] = reversed_token[:i][::-1]
        if i > 4 :
            break

    return features

# word shape feature example
def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower' 
    elif token.istitle() :
        return 'title'
    elif token.isalpha() :
        return 'mixed'
    else :
        return False

# vowel ratio feature example
def vowelRatio(token) :
    n_chars = len(token)
    if n_chars > 1:
        n_vowels = sum(token.count(c) for c in VOWELS_Y)
        return n_vowels/float(n_chars)
    else :
        return False

