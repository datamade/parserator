from lxml import etree
import sys
import os.path
import data_prep_utils
import re
import csv
from argparse import ArgumentParser
import unidecode


def consoleLabel(raw_strings, labels, module): 
    print '\nStart console labeling!\n'
    print 'These are the tags available for labeling:'
    valid_input_tags = dict((str(i), label) for i, label in enumerate(labels))
    for i in range(len(labels)):
        print '%s : %s' %(i, valid_input_tags[str(i)])
    print '\n\n'
    valid_responses = ['y', 'n', 's', 'f', '']
    finished = False

    strings_left_to_tag = raw_strings.copy()
    total_strings = len(raw_strings)
    tagged_strings = set([])

    for i, raw_sequence in enumerate(raw_strings, 1):

        if not finished:

            print '(%s of %s)' % (i, total_strings)
            print '-'*50
            print 'STRING: %s' %raw_sequence
            
            preds = module.parse(raw_sequence)

            user_input = None 
            while user_input not in valid_responses :

                friendly_repr = [(token[0], token[1]) for token in preds]
                print_table(friendly_repr)

                sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip / (f)inish tagging\n')
                user_input = sys.stdin.readline().strip()

                if user_input =='y':
                    tagged_strings.add(tuple(preds))
                    strings_left_to_tag.remove(raw_sequence)

                elif user_input =='n':
                    corrected_string = manualTagging(preds, 
                                                labels)
                    tagged_strings.add(tuple(corrected_string))
                    strings_left_to_tag.remove(raw_sequence)


                elif user_input in ('' or 's') :
                    print 'Skipped\n'
                elif user_input == 'f':
                    finished = True

    print 'Done! Yay!'
    return tagged_strings, strings_left_to_tag


def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "| %s |" % " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line))
        

def manualTagging(preds, labels):
    valid_input_tags = dict( (str(i), label) for i, label in enumerate(labels))
    tagged_sequence = []
    for token_pred in preds:
        valid_tag = False
        while not valid_tag:
            print 'What is \'%s\' ? If %s hit return' %(token_pred[0], token_pred[1])
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags or user_input_tag == '':
                valid_tag = True
            elif user_input_tag == 'help':
                print 'These are the valid inputs:'
                for i in range(len(label_options)):
                    print '%s : %s' %(i, valid_input_tags[str(i)])
            else:
                print "That is not a valid tag. Type 'help' to see the valid inputs"

        xml_tag = ''
        if user_input_tag == '':
            xml_tag = token_pred[1]
        else:
            xml_tag = labels[int(user_input_tag)]

        tagged_sequence.append((token_pred[0], xml_tag))
    return tagged_sequence


def naiveConsoleLabel(raw_strings, labels, module): 

    print '\nStart console labeling!\n'
    print 'These are the tags available for labeling:'
    valid_input_tags = dict((str(i), label) for i, label in enumerate(labels))
    for i in range(len(labels)):
        print '%s : %s' %(i, valid_input_tags[str(i)])
    print '\n\n'

    valid_responses = ['t', 's', 'f', '']
    finished = False

    strings_left_to_tag = raw_strings.copy()
    total_strings = len(raw_strings)
    tagged_strings = set([])

    for i, raw_sequence in enumerate(raw_strings, 1):
        if not finished:

            print '(%s of %s)' % (i, total_strings)
            print '-'*50
            print 'STRING: %s' %raw_sequence
            
            tokens = module.tokenize(raw_sequence)

            user_input = None 
            while user_input not in valid_responses :

                sys.stderr.write('(t)ag / (s)kip / (f)inish tagging\n')
                user_input = sys.stdin.readline().strip()

                if user_input =='t' or user_input == '':
                    tagged_sequence = naiveManualTag(tokens, labels)
                    tagged_strings.add(tuple(tagged_sequence))
                    strings_left_to_tag.remove(raw_sequence)

                elif user_input == 's':
                    print 'Skipped\n'
                elif user_input == 'f':
                    finished = True

    print 'Done! Yay!'
    return tagged_strings, strings_left_to_tag

def naiveManualTag(raw_sequence, labels):
    valid_input_tags = dict((str(i), label) for i, label in enumerate(labels))
    sequence_labels = []
    for token in raw_sequence:
        valid_tag = False
        while not valid_tag:
            print 'What is \'%s\' ?' %token
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags:
                valid_tag = True
            elif user_input_tag == 'help':
                print 'These are the valid inputs:'
                for i in range(len(labels)):
                    print '%s : %s' %(i, valid_input_tags[str(i)])
            else:
                print "That is not a valid tag. Type 'help' to see the valid inputs"
            
        token_label = labels[int(user_input_tag)]
        sequence_labels.append((token, token_label))
    return sequence_labels


def getArgumentParser():
    arg_parser = ArgumentParser(description="Label some strings")
    arg_parser.add_argument(dest="infile", 
                            help="input csv", metavar="FILE")
    arg_parser.add_argument(dest="outfile", 
                            help="output csv", metavar="FILE")
    arg_parser.add_argument("-n",
                            help="-n for naive labeling (if there isn't an existing .crfsuite settings file)", action="store_true")
    return arg_parser



def label(module, infile, outfile):

    file_slug = re.sub('(.*/)|(.csv)|(unlabeled_)', '', infile)
    unlabeled_dir = re.sub('[^/]+$', '', infile)

    # Check to make sure we can write to outfile
    if os.path.isfile(outfile):
        with open(outfile, 'r+' ) as f:
            try :
                tree = etree.parse(f)
            except :
                raise ValueError("%s does not seem to be a valid xml file"
                                 % outfile)

    with open(infile, 'rU') as f :
        reader = csv.reader(f)

        strings = set([unidecode.unidecode(row[0]) for row in reader])

    labels = module.LABELS

    try:
        labeled_list, raw_strings_left = consoleLabel(strings, labels, module) 
    except IOError:
        labeled_list, raw_strings_left = naiveConsoleLabel(strings, labels, module)

    data_prep_utils.appendListToXMLfile(labeled_list, module, outfile)
    data_prep_utils.list2file(raw_strings_left, unlabeled_dir+'unlabeled_'+file_slug+'.csv')

