#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import io
import sys

from lxml import etree

if sys.version < '3' :
    from backports import csv
else :
    import csv


# appends a labeled list to an existing xml file
# calls: appendListToXML, stripFormatting
def appendListToXMLfile(labeled_list, module, filepath):
    # format for labeled_list:      [   [ (token, label), (token, label), ...],
    #                                   [ (token, label), (token, label), ...],
    #                                   [ (token, label), (token, label), ...],
    #                                   ...           ]

    if os.path.isfile(filepath):
        with io.open(filepath) as f:
            tree = etree.parse(filepath)
            collection_XML = tree.getroot()
            collection_XML = stripFormatting(collection_XML)

    else:
        collection_tag = module.GROUP_LABEL
        collection_XML = etree.Element(collection_tag)

    parent_tag = module.PARENT_LABEL
    collection_XML = appendListToXML(labeled_list, collection_XML, parent_tag)

    with io.open(filepath, 'w') as f :
        f.write(etree.tostring(collection_XML, pretty_print = True).decode('utf-8'))


# given a list of labeled sequences to an xml list, 
# appends corresponding xml to existing xml
# calls: sequence2XML
# called by: appendListToXMLfile
def appendListToXML(list_to_append, collection_XML, parent_tag) :
    # format for list_to_append:    [   [ (token, label), (token, label), ...],
    #                                   [ (token, label), (token, label), ...],
    #                                   [ (token, label), (token, label), ...],
    #                                   ...           ]
    for labeled_sequence in list_to_append:
        sequence_xml = sequence2XML(labeled_sequence, parent_tag)
        collection_XML.append(sequence_xml)
    return collection_XML


# given a labeled sequence, generates xml for that sequence
# called by: appendListToXML
def sequence2XML(labeled_sequence, parent_tag) :
    # format for labeled_sequence:  [(token, label), (token, label), ...]

    sequence_xml = etree.Element(parent_tag)

    for token, label in labeled_sequence:
        component_xml = etree.Element(label)
        component_xml.text = token
        component_xml.tail = ' '
        sequence_xml.append(component_xml)
    sequence_xml[-1].tail = ''
    return sequence_xml


# clears formatting for an xml collection
def stripFormatting(collection) :
    collection.text = None 
    for element in collection :
        element.text = None
        element.tail = None
        
    return collection


# writes a list of strings to a file
def list2file(string_list, filepath):
    with io.open(filepath, 'w') as csvfile:
        writer = csv.writer(csvfile, doublequote=True, quoting=csv.QUOTE_MINIMAL)
        for string in string_list:
            writer.writerow([string])
