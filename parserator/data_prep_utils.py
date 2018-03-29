#!/usr/bin/python
# -*- coding: utf-8 -*-

from builtins import open

import os
import sys

from lxml import etree

if sys.version < '3' :
    from backports import csv
else :
    import csv


class TrainingData(object):
    def __init__(self, xml=None, module=None):

        if xml is not None:
            self.xml = xml
            self._strip_formatting(self.xml)
        else:
            collection_tag = module.GROUP_LABEL
            self.xml = etree.Element(collection_tag)

        if module:
            self.parent_tag = module.PARENT_LABEL

    def append(self, labeled_sequence):
        self.xml.append(self._sequence_to_xml(labeled_sequence))

    def extend(self, labeled_sequences):
        for labeled_sequence in labeled_sequences:
            self.append(labeled_sequence)

    def write(self, outfile):
        etree.ElementTree(self.xml).write(outfile, pretty_print=True)

    def _sequence_to_xml(self, labeled_sequence):
        sequence_xml = etree.Element(self.parent_tag)

        for token, label in labeled_sequence:
            component_xml = etree.Element(label)
            component_xml.text = token
            component_xml.tail = ' '
            sequence_xml.append(component_xml)

        sequence_xml[-1].tail = ''

        return sequence_xml

    def _xml_to_sequence(self, sequence_xml):
        return tuple((element.text, element.tag) for element in sequence_xml)

    # clears formatting for an xml collection
    def _strip_formatting(self, xml):
        xml.text = None
        for element in xml:
            element.text = None
            element.tail = None

    def __iter__(self):
        for sequence_xml in self.xml:
            raw_text = etree.tostring(sequence_xml, method='text', encoding='unicode')
            yield raw_text, self._xml_to_sequence(sequence_xml)


# writes a list of strings to a file
def list2file(string_list, filepath):
    with open(filepath, 'w') as csvfile:
        writer = csv.writer(csvfile, doublequote=True, quoting=csv.QUOTE_MINIMAL)
        for string in string_list:
            writer.writerow([string])
