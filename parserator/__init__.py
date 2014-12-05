import os
from training import train
import pycrfsuite
import warnings
from collections import OrderedDict


class Parser(object):

    LABELS = []

    ########################################
    ######## OPTIONAL CONFIG ###############
    ########################################
    NULL_LABEL = 'Null'
    # this is the xml tag for each string in training data. example: PARENT_LABEL = 'Name'
    PARENT_LABEL = 'TokenSequence'
    # this is the tag for a group of strings. example: GROUP_LABEL = 'NameCollection'
    GROUP_LABEL = 'Collection'
    # filename for settings file
    MODEL_FILE = 'learned_settings.crfsuite'
    MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE
    # filename for training data (from which the model is produced)
    TRAINING_FILE = 'labeled.xml' ########## should this be set here?

    VOWELS_Y = tuple('aeiouy')

    def __init__(self):
        try :
            self.TAGGER = pycrfsuite.Tagger()
            # path = os.path.split(os.path.abspath(__file__))[0] + '/' + self.MODEL_FILE
            self.TAGGER.open(self.MODEL_PATH)
        except IOError :
            warnings.warn("You must train the model (run training/training.py) and create the "+config.MODEL_FILE+" file before you can use the parse and tag methods")

    def parse(self, raw_string):
        tokens = self.tokenize(raw_string)

        if not tokens :
            return []

        features = self.tokens2features(tokens)

        try :
            self.TAGGER = pycrfsuite.Tagger()
            # path = os.path.split(os.path.abspath(__file__))[0] + '/' + self.MODEL_FILE
            self.TAGGER.open(self.MODEL_PATH)
        except IOError :
            warnings.warn("You must train the model (run training/training.py) and create the "+config.MODEL_FILE+" file before you can use the parse and tag methods")

        tags = self.TAGGER.tag(features)
        return zip(tokens, tags)

    def tag(self, raw_string) :
        print "in tag"
        tagged = OrderedDict()
        for token, label in self.parse(raw_string) :
            tagged.setdefault(label, []).append(token)

        for token in tagged :
            component = ' '.join(tagged[token])
            component = component.strip(" ,;")
            tagged[token] = component

        return tagged

    def tokenize(self, raw_string):
        raise NotImplementedError

    def tokens2features(self, tokens):
        raise NotImplementedError

    def tokenFeatures(self, token) :
        raise NotImplementedError

