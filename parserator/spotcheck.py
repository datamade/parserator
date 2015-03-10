#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import zip
import pycrfsuite

def compareTaggers(model1, model2, string_list, module_name):
    """
    Compare two models. Given a list of strings, prints out tokens & tags
    whenever the two taggers parse a string differently. This is for spot-checking models
    :param tagger1: a .crfsuite filename
    :param tagger2: another .crfsuite filename
    :param string_list: a list of strings to be checked
    :param module_name: name of a parser module
    """
    module = __import__(module_name)

    tagger1 = pycrfsuite.Tagger()
    tagger1.open(module_name+'/'+model1)
    tagger2 = pycrfsuite.Tagger()
    tagger2.open(module_name+'/'+model2)

    count_discrepancies = 0

    for string in string_list:
        tokens = module.tokenize(string)
        if tokens:
            features = module.tokens2features(tokens)

            tags1 = tagger1.tag(features)
            tags2 = tagger2.tag(features)

            if tags1 != tags2:
                count_discrepancies += 1
                print('\n')
                print("%s. %s" %(count_discrepancies, string))
                
                print('-'*75)
                print_spaced('token', model1, model2)
                print('-'*75)
                for token in zip(tokens, tags1, tags2):
                    print_spaced(token[0], token[1], token[2])
    print("\n\n%s of %s strings were labeled differently"%(count_discrepancies, len(string_list)))


def print_spaced(s1, s2, s3):
    n = 25
    print(s1 + " "*(n-len(s1)) + s2 + " "*(n-len(s2)) + s3)

def validateTaggers(model1, model2, labeled_string_list, module_name):

    module = __import__(module_name)

    tagger1 = pycrfsuite.Tagger()
    tagger1.open(module_name+'/'+model1)
    tagger2 = pycrfsuite.Tagger()
    tagger2.open(module_name+'/'+model2)

    wrong_count_1 = 0
    wrong_count_2 = 0
    wrong_count_both = 0
    correct_count = 0

    for labeled_string in labeled_string_list:
        unlabeled_string, components = labeled_string
        tokens = module.tokenize(unlabeled_string)
        if tokens:
            features = module.tokens2features(tokens)

            _, tags_true = list(zip(*components))
            tags_true = list(tags_true)
            tags1 = tagger1.tag(features)
            tags2 = tagger2.tag(features)

            if (tags1 != tags_true) and (tags2 != tags_true):
                print("\nSTRING: ", unlabeled_string)
                print("TRUE: ", tags_true)
                print("*%s: "%model1, tags1)
                print("*%s: "%model2, tags2)
                wrong_count_both += 1
            elif (tags1 != tags_true):
                print("\nSTRING: ", unlabeled_string)
                print("TRUE: ", tags_true)
                print("*%s: "%model1, tags1)
                print("%s: "%model2, tags2)
                wrong_count_1 += 1
            elif (tags2 != tags_true):
                print("\nSTRING: ", unlabeled_string)
                print("TRUE: ", tags_true)
                print("%s: "%model1, tags1)
                print("*%s: "%model2, tags2)
                wrong_count_2 += 1
            else:
                correct_count += 1

    print("\n\nBOTH WRONG: ", wrong_count_both)
    print("%s WRONG: %s" %(model1, wrong_count_1))
    print("%s WRONG: %s" %(model2, wrong_count_2))
    print("BOTH CORRECT: ", correct_count)


