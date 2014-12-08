import pycrfsuite
import random
import os
from lxml import etree
from imp import reload
import data_prep_utils


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


# given a list of xml training files (in TRAINING_DATA_DIR) & a parser object,
# reads the xml & returns training data (for trainModel)
def readTrainingData( xml_infile_list, p ):

    collection_tag = p.GROUP_LABEL
    full_xml = etree.Element(collection_tag)
    component_string_list = []

    # loop through xml training files
    for xml_infile in xml_infile_list:
        train_data_filepath = p.TRAINING_DATA_DIR + '/' + xml_infile
        if os.path.isfile(train_data_filepath):
            with open( train_data_filepath, 'r+' ) as f:
                tree = etree.parse(f)
                file_xml = tree.getroot()
                file_xml = data_prep_utils.stripFormatting(file_xml)
                for component_etree in file_xml:
                    # etree components to string representations
                    component_string_list.append(etree.tostring(component_etree))
        else:
            print "WARNING: %s does not exist" % xml_infile
    # get rid of duplicates in string representations
    component_string_list = list(set(component_string_list))

    # loop through unique string representations
    for component_string in component_string_list:
        # convert string representation back to xml
        sequence_xml = etree.fromstring(component_string)
        raw_text = etree.tostring(sequence_xml, method='text')
        sequence_components = []
        for component in list(sequence_xml):
            sequence_components.append([component.text, component.tag])

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


def train(parser, train_file_list) :

    training_data = list(readTrainingData(train_file_list, parser))
    print "training model on %s training examples" %len(training_data)

    trainModel(training_data, parser)
    print "done training!"
