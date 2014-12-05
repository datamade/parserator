import pycrfsuite
import random
import os
from lxml import etree
from imp import reload


def trainModel(training_data, parser,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

    X = []
    Y = []

    for raw_string, components in training_data:
        tokens, labels = zip(*components)
        X.append(parser.tokens2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(parser.MODEL_PATH)

def readTrainingData(filepath):
    tree = etree.parse(filepath)
    collection = tree.getroot()

    for sequence in collection:
        sequence_components = []
        raw_text = etree.tostring(sequence, method='text')
        raw_text = raw_text.replace('&#38;', '&')
        for component in list(sequence):
            sequence_components.append([component.text, component.tag])
            if component.tail and component.tail.strip():
                sequence_components.append([component.tail.strip(), config.NULL_TAG])

        yield raw_text, sequence_components


def get_data_sklearn_format(path='training/training_data/labeled.xml'):
    """
    Parses the specified data file and returns it in sklearn format.
    :param path:
    :return: tuple of:
                1) list of training sequences, each of which is a string
                2) list of gold standard labels, each of which is a tuple
                of strings, one for each token in the corresponding training
                sequence
    """
    data = list(readTrainingData(path))
    random.shuffle(data)

    x, y = [], []
    for raw_string, components in data:
        tokens, labels = zip(*components)
        x.append(raw_string)
        y.append(labels)
    return x, y


def train(parser) :

    train_data_filepath = parser.TRAINING_DATA_DIR + '/' + parser.TRAINING_FILE
    training_data = list(readTrainingData(train_data_filepath))

    trainModel(training_data, parser)



if __name__ == '__main__':

    root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    training_data = list(readTrainingData(root_path + '/training/training_data/' + config.TRAIN_DATA))

    trainModel(training_data, root_path + '/parserator/' + config.MODEL_FILE)
