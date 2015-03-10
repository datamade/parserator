#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from parserator.data_prep_utils import sequence2XML
from lxml import etree
import unittest

class TestList2XML(unittest.TestCase) :

    def test_xml(self):
        XMLequals( [('#', 'foo'), ('1', 'foo'), ('Pinto', 'foo')], '<foo>#</foo> <foo>1</foo> <foo>Pinto</foo>')

    def test_none_tag(self):
        XMLequals( [('Box', 'foo'), ('#', 'Null'), ('1', 'foo'), ('Pinto', 'foo')], '<foo>Box</foo> <Null>#</Null> <foo>1</foo> <foo>Pinto</foo>')
        XMLequals( [('#', 'Null'), ('1', 'foo'), ('Pinto', 'foo')], '<Null>#</Null> <foo>1</foo> <foo>Pinto</foo>')
       
       
def XMLequals(labeled_sequence, xml):
    correct_xml = '<TokenSequence>' + xml + '</TokenSequence>'
    generated_xml = etree.tostring( sequence2XML(labeled_sequence, 'TokenSequence') ).decode('utf-8')
    print('Correct:   %s' %correct_xml)
    print('Generated: %s' %generated_xml)
    assert correct_xml == generated_xml


if __name__ == '__main__' :
    unittest.main()    
