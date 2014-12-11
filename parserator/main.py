from argparse import ArgumentParser
import manual_labeling
import training
import os
import shutil
import fileinput
from parser_template import init_template, setup_template, test_tokenize_template


def dispatch():

    parser = ArgumentParser(description="")
    parser.add_argument(dest='module_name')
    parser.add_argument(dest="command", help="init, label, or train")
    parser.add_argument("--infile",
                        help="input csv filepath for the label task", metavar="FILEPATH")
    parser.add_argument("--outfile",
                        help="output xml filepath for the label task", metavar="FILEPATH")
    parser.add_argument("--name",
                        help="module name for a new parser")
    parser.add_argument("--traindata",
                        help="comma separated xml filepaths", metavar="FILEPATH")
    args = parser.parse_args()

    print args.command

    if args.command == 'label':
        label(args)
    elif args.command == 'train':
        train(args)
    elif args.command == 'init':
        init(args)
    else :
        print 'help'

def label(args) :
    if args.infile and args.outfile:
        module = __import__(args.module_name)
        infile_path = args.infile
        outfile_path = args.outfile
        manual_labeling.label(module, infile_path, outfile_path)
    else:
        print 'Please specify an input csv file [--infile FILE] and an output xml file [--outfile FILE]'


def train(args) :
    if args.traindata:
        train_file_list = args.traindata.split(',')
        module = __import__(args.module_name)
        
        training.train(module, train_file_list)
    else:
        print 'Please specify one or more xml training files (comma separated) [--trainfile FILE]'


def init(args) :
    name = args.module_name
    data = "raw"
    training = "training"
    tests = 'tests'
    
    dirs_to_mk = [name, data, training, tests]

    print '\nInitializing directories for %s' %name
    for directory in dirs_to_mk:
        if not os.path.exists(directory):
            os.mkdir(directory)
            print '* %s' %directory

    print '\nGenerating __init__.py'
    init_path = name + '/__init__.py'

    if os.path.exists(init_path):
        print '  warning: %s already exists' %init_path
    else:
        with open(init_path, "w") as f:
            f.write(init_template())
        print '* %s' %init_path

    print '\nGenerating setup.py'
    if os.path.exists('setup.py'):
        print '  warning: setup.py already exists'
    else:
        with open('setup.py', 'w') as f:
            f.write(setup_template(name))
        print '* setup.py'

    print '\nGenerating test file'
    token_test_path = tests+'/test_tokenizing.py'
    if os.path.exists(token_test_path):
        print '  warning: %s already exists' %token_test_path
    else:
        with open(token_test_path, 'w') as f:
            f.write(test_tokenize_template(name))
        print '* %s' %token_test_path


