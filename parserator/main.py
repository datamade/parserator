from argparse import ArgumentParser
import manual_labeling
import training
import os
import shutil
import fileinput


def dispatch():

    parser = ArgumentParser(description="")
    parser.add_argument(dest="command", help="init, label, or train")
    parser.add_argument(dest='module_name')
    parser.add_argument("--infile",
                        help="input csv for the label task", metavar="FILE")
    parser.add_argument("--outfile",
                        help="output xml for the label task", metavar="FILE")
    parser.add_argument("--name",
                        help="module name for a new parser")
    args = parser.parse_args()


    

    if args.command == 'label':
        if args.infile and args.outfile:
            m = __import__(args.module_name, ["Parser"])
            p = m.Parser()
            infile_path = p.UNLABELED_DATA_DIR + '/' + args.infile
            outfile_path = p.TRAINING_DATA_DIR + '/' + args.outfile
            manual_labeling.label(p, infile_path, outfile_path)
        else:
            print "Please specify an input csv file [--infile FILE] and an output xml file [--outfile FILE]"

    elif args.command == 'train':
        m = __import__(args.module_name, ["Parser"])
        p = m.Parser()
        training.train(p)

    elif args.command == 'init':
        name = args.module_name
        data = args.module_name + "_data"
        unlabeled = data + '/unlabeled'
        labeled = data + '/labeled_xml'

        dirs_to_mk = [name, data, unlabeled, labeled]

        print "\nInitializing directories for", name
        for directory in dirs_to_mk:
            if not os.path.exists(directory):
                os.mkdir(directory)
                print "* ", directory

        print "\nGenerating __init__.py"
        init_path = name + "/__init__.py"
        if os.path.exists(init_path):
            print "  warning:", init_path, "already exists"
        else:
            shutil.copyfile("parserator/parser_template.txt", init_path)
            for line in fileinput.input(init_path, inplace=True):
                print(line.replace('MODULENAME', name).rstrip())
            print "* ", init_path



