from argparse import ArgumentParser
import manual_labeling
import training
import os
import shutil
import fileinput
from parser_template import template


def dispatch():

    parser = ArgumentParser(description="")
    parser.add_argument(dest="command", help="init, label, or train")
    parser.add_argument(dest='module_name')
    parser.add_argument("--infile",
                        help="input csv filepath for the label task", metavar="FILEPATH")
    parser.add_argument("--outfile",
                        help="output xml filepath for the label task", metavar="FILEPATH")
    parser.add_argument("--name",
                        help="module name for a new parser")
    parser.add_argument("--traindata",
                        help="comma separated xml filepaths", metavar="FILEPATH")
    args = parser.parse_args()


    if args.command == 'label':
        if args.infile and args.outfile:
            m = __import__(args.module_name, ["Parser"])
            infile_path = args.infile
            outfile_path = args.outfile
            manual_labeling.label(m, infile_path, outfile_path)
        else:
            print 'Please specify an input csv file [--infile FILE] and an output xml file [--outfile FILE]'

    elif args.command == 'train':
        if args.traindata:
            train_file_list = args.traindata.split(',')
            m = __import__(args.module_name, ["Parser"])

            training.train(m, train_file_list)
        else:
            print 'Please specify one or more xml training files (comma separated) [--trainfile FILE]'

    elif args.command == 'init':
        name = args.module_name
        data = args.module_name + "_data"
        unlabeled = data + '/unlabeled'
        labeled = data + '/labeled_xml'

        dirs_to_mk = [name, data, unlabeled, labeled]

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
                f.write(template())

            for line in fileinput.input(init_path, inplace=True):
                print(line.replace('MODULENAME', name).rstrip())
            print '* %s' %init_path



