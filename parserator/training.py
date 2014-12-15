import pycrfsuite
import random
import os
from lxml import etree
from imp import reload
import data_prep_utils


def trainModel(training_data, module,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

    X = []
    Y = []

    for raw_string, components in training_data:
        tokens, labels = zip(*components)
        X.append(module.tokens2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(module.__name__+'/'+module.MODEL_FILE)


# given a list of xml training filepaths & a parser module,
# reads the xml & returns training data (for trainModel)
def readTrainingData( xml_infile_list, collection_tag ):

    full_xml = etree.Element(collection_tag)
    component_string_list = []

    # loop through xml training files
    for xml_infile in xml_infile_list:
        train_data_filepath = xml_infile
        if os.path.isfile(train_data_filepath):
            with open( train_data_filepath, 'r+' ) as f:
                tree = etree.parse(f)
                file_xml = tree.getroot()
                file_xml = data_prep_utils.stripFormatting(file_xml)
                for component_etree in file_xml:
                    # etree components to string representations
                    component_string_list.append(etree.tostring(component_etree))
        else:
            print 'WARNING: %s does not exist' % xml_infile
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


def train(module, train_file_list) :

    training_data = list(readTrainingData(train_file_list, module.GROUP_LABEL))
    print 'training model on %s training examples' %len(training_data)

    trainModel(training_data, module)
    print 'done training!'
