import os
import re
import textwrap
import time

import pycrfsuite
from lxml import etree

from . import data_prep_utils


def trainModel(
    training_data,
    module,
    model_path,
    params_to_set={"c1": 0.1, "c2": 0.01, "feature.minfreq": 0},
):

    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)

    for _, components in training_data:
        tokens, labels = list(zip(*components))
        trainer.append(module.tokens2features(tokens), labels)

    trainer.train(model_path)


def renameModelFile(old_model):
    if os.path.exists(old_model):
        t = time.gmtime(os.path.getctime(old_model))
        time_str = time.strftime("_%Y_%m_%d_%H_%M_%S", t)
        new_name = re.sub(".crfsuite", time_str + ".crfsuite", old_model)
        msg = """
              renaming old model: %s -> %s"""
        print(textwrap.dedent(msg % (old_model, new_name)))
        os.rename(old_model, new_name)


def train(module, training_data, model_path):

    renameModelFile(model_path)

    trainModel(training_data, module, model_path)

    msg = """
          done training! model file created: {path}""".format(
        path=model_path
    )

    print(textwrap.dedent(msg))


def readTrainingData(file_locations, GROUP_LABEL):
    """
    Used in downstream tests
    """

    class Mock:
        pass

    mock_module = Mock()
    mock_module.PARENT_LABEL = GROUP_LABEL
    for location in file_locations:
        with open(location) as f:
            tree = etree.parse(f)

        xml = tree.getroot()
        yield from data_prep_utils.TrainingData(xml, mock_module)
