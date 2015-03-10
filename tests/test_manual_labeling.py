#!/usr/bin/python
# -*- coding: utf-8 -*-

from parserator.data_prep_utils import sequence2XML
from lxml import etree
import unittest

class TestManualsequence2XML(unittest.TestCase) :

    def test_single_component(self) :

        test_input = [ ('bob', 'foo') ]
        expected_xml = '<TokenSequence><foo>bob</foo></TokenSequence>'
        assert etree.tostring( sequence2XML(test_input, 'TokenSequence') ).decode('utf-8') == expected_xml

    def test_two_components(self) :

        test_input = [ ('bob', 'foo'), ('b', 'bar') ]
        expected_xml = '<TokenSequence><foo>bob</foo> <bar>b</bar></TokenSequence>'
        assert etree.tostring( sequence2XML(test_input, 'TokenSequence') ).decode('utf-8') == expected_xml

    def test_multiple_components(self) :

        test_input = [ ('bob', 'foo'), ('b', 'bar'), ('sr', 'foobar') ]
        expected_xml = '<TokenSequence><foo>bob</foo> <bar>b</bar> <foobar>sr</foobar></TokenSequence>'

        assert etree.tostring( sequence2XML(test_input, 'TokenSequence') ).decode('utf-8') == expected_xml


if __name__ == '__main__' :
    unittest.main()    
