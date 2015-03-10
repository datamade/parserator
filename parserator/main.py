#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from argparse import ArgumentParser
from . import manual_labeling
from . import training
import os
import shutil
import fileinput
from .parser_template import init_template, setup_template, test_tokenize_template


def dispatch():

    parser = ArgumentParser(description="")
    parser_subparsers = parser.add_subparsers()
    sub_label = parser_subparsers.add_parser('label')
    sub_train = parser_subparsers.add_parser('train')
    sub_init = parser_subparsers.add_parser('init')

    sub_label.add_argument(dest='infile', help='input csv filepath for the label task')
    sub_label.add_argument(dest='outfile', help='output xml filepath for the label task')
    sub_label.add_argument(dest='modulename', help='parser module name')
    sub_label.set_defaults(func=label)

    sub_train.add_argument(dest='traindata', help='comma separated xml filepaths')
    sub_train.add_argument(dest='modulename', help='parser module name')
    sub_train.set_defaults(func=train)

    sub_init.add_argument(dest='modulename', help='module name for a new parser')
    sub_init.set_defaults(func=init)

    args = parser.parse_args()

    args.func(args)


def label(args) :
    if args.infile and args.outfile:
        module = __import__(args.modulename)
        infile_path = args.infile
        outfile_path = args.outfile
        manual_labeling.label(module, infile_path, outfile_path)
    else:
        print('Please specify an input csv file [--infile FILE] and an output xml file [--outfile FILE]')


def train(args) :
    if args.traindata:
        train_file_list = args.traindata.split(',')
        module = __import__(args.modulename)
        
        training.train(module, train_file_list)
    else:
        print('Please specify one or more xml training files (comma separated) [--trainfile FILE]')


def init(args) :
    name = args.modulename
    data = "raw"
    training = "training"
    tests = 'tests'
    
    dirs_to_mk = [name, data, training, tests]

    print('\nInitializing directories for %s' %name)
    for directory in dirs_to_mk:
        if not os.path.exists(directory):
            os.mkdir(directory)
            print('* %s' %directory)

    print('\nGenerating __init__.py')
    init_path = name + '/__init__.py'

    if os.path.exists(init_path):
        print('  warning: %s already exists' %init_path)
    else:
        with open(init_path, "w") as f:
            f.write(init_template())
        print('* %s' %init_path)

    print('\nGenerating setup.py')
    if os.path.exists('setup.py'):
        print('  warning: setup.py already exists')
    else:
        with open('setup.py', 'w') as f:
            f.write(setup_template(name))
        print('* setup.py')

    print('\nGenerating test file')
    token_test_path = tests+'/test_tokenizing.py'
    if os.path.exists(token_test_path):
        print('  warning: %s already exists' %token_test_path)
    else:
        with open(token_test_path, 'w') as f:
            f.write(test_tokenize_template(name))
        print('* %s' %token_test_path)


