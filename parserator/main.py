#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

from argparse import ArgumentParser, ArgumentTypeError
import os
import shutil
import fileinput
import sys
import glob

from . import manual_labeling
from . import training
from . import parser_template

def dispatch():

    parser = ArgumentParser(description="")
    parser_subparsers = parser.add_subparsers()

    # Arguments for label command
    sub_label = parser_subparsers.add_parser('label')
    sub_label.add_argument(dest='infile',
                           help='input csv filepath for the label task')
    sub_label.add_argument(dest='outfile',
                           help='output xml filepath for the label task')
    sub_label.add_argument(dest='modulename',
                           help='parser module name')
    sub_label.set_defaults(func=label)

    # Arguments for train command
    sub_train = parser_subparsers.add_parser('train')
    sub_train.add_argument(dest='traindata',
                           help='comma separated xml filepaths, or "path/to/traindata/*.xml"',
                           type=training_files)
    sub_train.add_argument(dest='modulename',
                           help='parser module name')
    sub_train.add_argument('--modelfile',
                           dest='modelfile',
                           help='location of model file',
                           required=False)
    sub_train.set_defaults(func=train)

    # Arguments for init command
    sub_init = parser_subparsers.add_parser('init')
    sub_init.add_argument(dest='modulename',
                          help='module name for a new parser')
    sub_init.set_defaults(func=init)

    args = parser.parse_args()

    args.func(args)

def training_files(arg):
    if ',' in arg:
        train_file_list = arg.split(',')
    else:
        train_file_list = glob.glob(arg)

    train_file_list = [f for f in train_file_list
                       if f.lower().endswith('.xml')]

    if not train_file_list:
        raise ArgumentTypeError('Please specify one or more xml training files (comma separated) [--trainfile FILE]')

    return train_file_list

    
def label(args) :
    module = __import__(args.modulename)
    infile_path = args.infile
    outfile_path = args.outfile
    manual_labeling.label(module, infile_path, outfile_path)

def train(args) :
    train_file_list = args.traindata
    module = __import__(args.modulename)
    modelfile = args.modelfile
    training.train(module, train_file_list, modelfile)


def init(args) :
    name = args.modulename
    data = "raw"
    training = "training"
    tests = 'tests'
    
    dirs_to_mk = [name, data, training, tests]

    print('\nInitializing directories for %s' %name, sys.stderr)
    for directory in dirs_to_mk:
        if not os.path.exists(directory):
            os.mkdir(directory)
            print('* %s' %directory, sys.stderr)

    print('\nGenerating __init__.py', sys.stderr)
    init_path = name + '/__init__.py'

    if os.path.exists(init_path):
        print('  warning: %s already exists' %init_path, sys.stderr)
    else:
        with open(init_path, "w") as f:
            f.write(parser_template.init_template())
        print('* %s' %init_path)

    print('\nGenerating setup.py')
    if os.path.exists('setup.py'):
        print('  warning: setup.py already exists', sys.stderr)
    else:
        with open('setup.py', 'w') as f:
            f.write(parser_template.setup_template(name))
        print('* setup.py', sys.stderr)

    print('\nGenerating test file', sys.stderr)
    token_test_path = tests+'/test_tokenizing.py'
    if os.path.exists(token_test_path):
        print('  warning: %s already exists' % token_test_path, sys.stderr)
    else:
        with open(token_test_path, 'w') as f:
            f.write(parser_template.test_tokenize_template(name))
        print('* %s' %token_test_path, sys.stderr)


