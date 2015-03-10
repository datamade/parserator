#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator
from sklearn.grid_search import GridSearchCV
from training import get_data_sklearn_format
import pycrfsuite


def f1_with_flattening(estimator, X, y):
    """
    Calculate F1 score by flattening the predictions of the
    estimator across all sequences. For example, given the following
    address sequences as input
        ['1 My str', '2 Your blvd'],
    the predictions of the model will be flattened like so:
        ['AddressNumber', 'StreetName', 'StreetNamePostType', 'AddressNumber', 'StreetName', 'StreetNamePostType']
    and compared to a similarly flattened gold standard labels. This calculates the overall
    quality of the model across all sequences as opposed to how well it does
    at any particular sequence.
    :param X: list of sequences to tag
    :param y: list of gold standard tuples
    """
    predicted = estimator.predict(X)
    flat_pred, flat_gold = [], []
    for a, b in zip(predicted, y):
        if len(a) == len(b):
            flat_pred.extend(a)
            flat_gold.extend(b)
    return f1_score(flat_gold, flat_pred)


def get_data_sklearn_format(train_file_list, module):
    """
    Parses the specified data files and returns it in sklearn format.
    :param path:
    :return: tuple of:
                1) list of training sequences, each of which is a string
                2) list of gold standard labels, each of which is a tuple
                of strings, one for each token in the corresponding training
                sequence
    """
    data = list(readTrainingData(train_file_list, module.GROUP_LABEL))
    random.shuffle(data)

    x, y = [], []
    for raw_string, components in data:
        tokens, labels = zip(*components)
        x.append(raw_string)
        y.append(labels)
    return x, y


class SequenceEstimator(BaseEstimator):
    """
    A sklearn-compatible wrapper for a parser trainer
    """

    def __init__(self, c1=1, c2=1, feature_minfreq=0):
        """
        :param c1: L1 regularisation coefficient
        :param c2: L2 regularisation coefficient
        :param feature_minfreq: minimum feature frequency
        :return:
        """
        self.c1 = c1
        self.c2 = c2
        self.feature_minfreq = feature_minfreq

    def fit(self, X, y, **params, model_path):
        # sklearn requires parameters to be declared as fields of the estimator,
        # an we can't have a full stop there. Replace with an underscore
        params = {k.replace('_', '.'): v for k, v in self.__dict__.items()}
        trainer = pycrfsuite.Trainer(verbose=False, params=params)
        for raw_text, labels in zip(X, y):
            tokens = tokenize(raw_text)
            trainer.append(tokens2features(tokens), labels)
        trainer.train(model_path)
        reload(parserator)

    def predict(self, X):
        reload(parserator)  # tagger object is defined at the module level, update now
        predictions = []
        for sequence in X:
            predictions.append([foo[1] for foo in parserator.parse(sequence)])
        return predictions


if __name__ == '__main__':
    # refer to http://www.chokkan.org/software/crfsuite/manual.html
    # for description of parameters
    cv = GridSearchCV(SequenceEstimator(), {'c1': [10 ** x for x in range(-2, 2)],
                                           'c2': [10 ** x for x in range(-2, 4)],
                                           'feature_minfreq': [0, 3, 5]},
                      scoring=f1_with_flattening, verbose=5)
    X, y = get_data_sklearn_format()
    cv.fit(X, y)
    print(cv.best_params_)
    for foo in cv.grid_scores_:
        print(foo)
