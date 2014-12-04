from argparse import ArgumentParser
import manual_labeling
import training


def dispatch():

    parser = ArgumentParser(description="")
    parser.add_argument(dest='module')
    parser.add_argument(dest="command", help="label or train")
    parser.add_argument("--infile",
                        help="input csv for the label task", metavar="FILE")
    parser.add_argument("--outfile",
                        help="output xml for the label task", metavar="FILE")
    args = parser.parse_args()


    m = __import__(args.module, ["Parser"])
    p = m.Parser()

    if args.command == 'label':
        if args.infile and args.outfile:
            infile_path = p.UNLABELED_DATA_DIR + '/' + args.infile
            outfile_path = p.TRAINING_DATA_DIR + '/' + args.outfile
            manual_labeling.label(p, infile_path, outfile_path)
        else:
            print "Please specify an input csv file [--infile FILE] and an output xml file [--outfile FILE]"

    elif args.command == 'train':
        training.train(p)
