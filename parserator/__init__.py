import os
from training import train
import pycrfsuite
import warnings
from collections import OrderedDict


class Parser(object):

    LABELS = []

    NULL_LABEL = 'Null'
    PARENT_LABEL = 'TokenSequence' # default xml tag for each string in training data
    GROUP_LABEL = 'Collection' # default tag for a group of strings
    MODEL_FILE = 'learned_settings.crfsuite' # default settings file
    MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE

    def __init__(self):
        try :
            self.TAGGER = pycrfsuite.Tagger()
            self.TAGGER.open(self.MODEL_PATH)
        except IOError :
            warnings.warn('You must train the model (parserator train --trainfile FILES) to create the %s file before you can use the parse and tag methods' %self.MODEL_FILE)

    def parse(self, raw_string):
        tokens = self.tokenize(raw_string)

        if not tokens :
            return []

        features = self.tokens2features(tokens)

        try :
            self.TAGGER = pycrfsuite.Tagger()
            self.TAGGER.open(self.MODEL_PATH)
        except IOError :
            warnings.warn('You must train the model (parserator train --trainfile FILES) to create the %s file before you can use the parse and tag methods' %self.MODEL_FILE)

        tags = self.TAGGER.tag(features)
        return zip(tokens, tags)

    def tag(self, raw_string) :
        tagged = OrderedDict()
        for token, label in self.parse(raw_string) :
            tagged.setdefault(label, []).append(token)

        for token in tagged :
            component = ' '.join(tagged[token])
            component = component.strip(' ,;')
            tagged[token] = component

        return tagged

    def tokenize(self, raw_string):
        raise NotImplementedError

    def tokens2features(self, tokens):
        raise NotImplementedError

    def tokenFeatures(self, token) :
        raise NotImplementedError

