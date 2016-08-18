#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
import pycrfsuite
import random
import os
from lxml import etree
from imp import reload
from . import data_prep_utils
import re
import time


def trainModel(training_data, module, model_path,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

    X = []
    Y = []

    for raw_string, components in training_data:
        tokens, labels = list(zip(*components))
        X.append(module.tokens2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(model_path)


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
            print('WARNING: %s does not exist' % xml_infile)
            # get rid of duplicates in string representations
            component_string_list = list(set(component_string_list))

    # loop through unique string representations
    for component_string in component_string_list:
        # convert string representation back to xml
        sequence_xml = etree.fromstring(component_string)
        raw_text = etree.tostring(sequence_xml, method='text', encoding='utf-8')
        sequence_components = []
        for component in list(sequence_xml):
            sequence_components.append([component.text, component.tag])

        yield raw_text, sequence_components


def renameModelFile(old_model):
    if os.path.exists(old_model):
        t = time.gmtime(os.path.getctime(old_model))
        time_str = '_'+str(t.tm_year)+'_'+str(t.tm_mon)+'_'+str(t.tm_mday)+'_'+str(t.tm_hour)+str(t.tm_min)+str(t.tm_sec)
        renamed = re.sub('.crfsuite', time_str+'.crfsuite', old_model)

        print("\nrenaming old model: %s -> %s" %(old_model, renamed))
        os.rename(old_model, renamed)


def train(module, train_file_list, model_file) :

    training_data = list(readTrainingData(train_file_list, module.GROUP_LABEL))
    if not training_data:
        print('ERROR: No training data found. Perhaps double check your training data filepaths?')
        return

    if model_file is None:
        model_path = module.__name__+'/'+module.MODEL_FILE
        if hasattr(module, 'MODEL_FILES'):
            print("\nNOTE: this parser allows for multiple model files")
            print("You can specify a model with the --modelfile argument")
            print("Models available:")
            for m in module.MODEL_FILES:
                print("  - %s" % m)
            print("Since no model was specified, we will train the default model")
    else:
        if hasattr(module, 'MODEL_FILES'):
            model_path = module.__name__+'/'+module.MODEL_FILES[model_file]
        else: # should this even be a fallback
            model_path = module.__name__+'/'+model_file
    renameModelFile(model_path)

    print('\ntraining model on {num} training examples from {file_list}'.format(num=len(training_data), file_list=train_file_list))

    trainModel(training_data, module, model_path)

    print('\ndone training! model file created: {path}'.format(path=model_path))
