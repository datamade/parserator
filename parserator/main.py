import argparse
import glob
import os
import sys
import textwrap

import chardet
from lxml import etree

from . import data_prep_utils, manual_labeling, parser_template, training


def dispatch():

    parser = argparse.ArgumentParser(description="")
    parser_subparsers = parser.add_subparsers()

    # Arguments for label command
    sub_label = parser_subparsers.add_parser("label")
    sub_label.add_argument(
        dest="infile", help="input csv filepath for the label task", type=file_type
    )
    sub_label.add_argument(
        dest="outfile", help="output xml filepath for the label task", action=XML
    )
    sub_label.add_argument(dest="module", help="parser module name", type=python_module)
    sub_label.set_defaults(func=label)

    # Arguments for train command
    sub_train = parser_subparsers.add_parser("train")
    sub_train.add_argument(
        dest="traindata",
        help='comma separated xml filepaths, or "path/to/traindata/*.xml"',
        type=training_data,
    )
    sub_train.add_argument(dest="module", help="parser module name", type=python_module)
    sub_train.add_argument(
        "--modelfile",
        dest="model_path",
        help="location of model file",
        action=ModelFile,
        required=False,
    )
    sub_train.set_defaults(func=train)

    # Arguments for init command
    sub_init = parser_subparsers.add_parser("init")
    sub_init.add_argument(dest="modulename", help="module name for a new parser")
    sub_init.set_defaults(func=init)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    args.func(args)


def label(args):
    manual_labeling.label(args.module, args.infile, args.outfile, args.xml)


def train(args):
    training_data = args.traindata
    module = args.module
    model_path = args.model_path

    if model_path is None:
        model_path = module.__name__ + "/" + module.MODEL_FILE
        if hasattr(module, "MODEL_FILES"):
            msg = """
                  NOTE: this parser allows for multiple model files
                  You can specify a model with the --modelfile argument
                  Models available:"""
            print(textwrap.dedent(msg))
            for m in module.MODEL_FILES:
                print("  - %s" % m)
            print("Since no model was specified, we will train the default model")

    training.train(module, training_data, model_path)


def init(args):
    name = args.modulename
    data = "raw"
    training = "training"
    tests = "tests"

    dirs_to_mk = [name, data, training, tests]

    print("\nInitializing directories for %s" % name, sys.stderr)
    for directory in dirs_to_mk:
        if not os.path.exists(directory):
            os.mkdir(directory)
            print("* %s" % directory, sys.stderr)

    print("\nGenerating __init__.py", sys.stderr)
    init_path = name + "/__init__.py"

    if os.path.exists(init_path):
        print("  warning: %s already exists" % init_path, sys.stderr)
    else:
        with open(init_path, "w") as f:
            f.write(parser_template.init_template())
        print("* %s" % init_path)

    print("\nGenerating setup.py")
    if os.path.exists("setup.py"):
        print("  warning: setup.py already exists", sys.stderr)
    else:
        with open("setup.py", "w") as f:
            f.write(parser_template.setup_template(name))
        print("* setup.py", sys.stderr)

    print("\nGenerating test file", sys.stderr)
    token_test_path = tests + "/test_tokenizing.py"
    if os.path.exists(token_test_path):
        print("  warning: %s already exists" % token_test_path, sys.stderr)
    else:
        with open(token_test_path, "w") as f:
            f.write(parser_template.test_tokenize_template(name))
        print("* %s" % token_test_path, sys.stderr)


class XML(argparse.Action):
    def __call__(self, parser, namespace, string, option_string):
        try:
            with open(string) as f:
                tree = etree.parse(f)
                xml = tree.getroot()
        except OSError:
            xml = None
        except etree.XMLSyntaxError as e:
            if "Document is empty" not in str(e):
                raise argparse.ArgumentError(
                    self, "%s does not seem to be a valid xml file" % string
                )
            xml = None

        setattr(namespace, self.dest, string)
        setattr(namespace, "xml", xml)


def file_type(arg):
    try:
        f = open(arg, "rb")
    except OSError as e:
        message = "can't open '%s': %s"
        raise argparse.ArgumentTypeError(message % (arg, e))
    else:
        detector = chardet.universaldetector.UniversalDetector()

        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break

        f.close()
        detector.close()

        f = open(arg, encoding=detector.result["encoding"])

    return f


def training_data(arg):
    all_files = []
    for path in arg.split(","):
        all_files.extend(glob.glob(path))

    xml_files = [
        f for f in all_files if (f.lower().endswith(".xml") and os.path.isfile(f))
    ]

    if not xml_files:
        raise argparse.ArgumentTypeError(
            "Please specify one or more xml training files (comma separated) [--trainfile FILE]"
        )

    training_data = set()
    for xml_file in xml_files:
        with open(xml_file) as f:
            try:
                tree = etree.parse(f)
            except etree.XMLSyntaxError:
                raise argparse.ArgumentTypeError(
                    "{} is not a valid xml file".format(f.name)
                )

            file_xml = tree.getroot()
            training_data.update(data_prep_utils.TrainingData(file_xml))

    if not training_data:
        raise argparse.ArgumentTypeError(
            "No training data found. Perhaps double check "
            "your training data filepaths?"
        )

    msg = """
          training model on {num} training examples from {file_list} file(s)"""

    print(textwrap.dedent(msg.format(num=len(training_data), file_list=xml_files)))

    return training_data


class ModelFile(argparse.Action):
    def __call__(self, parser, namespace, model_file, option_string):
        module = namespace.module

        if hasattr(module, "MODEL_FILES"):
            try:
                model_path = module.__name__ + "/" + module.MODEL_FILES[model_file]
            except KeyError:
                msg = """
                      Invalid --modelfile argument
                      Models available: %s"""
                raise argparse.ArgumentTypeError(
                    textwrap.dedent(msg) % module.MODEL_FILES
                )
        else:
            raise argparse.ArgumentError(
                self, "This parser does not allow for multiple models"
            )

        setattr(namespace, self.dest, model_path)


def python_module(arg):
    module = __import__(arg)
    return module
