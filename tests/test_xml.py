import unittest

from lxml import etree

from parserator import data_prep_utils


class Mock:
    pass


class TestList2XML(unittest.TestCase):
    def setUp(self):
        mock_module = Mock()
        mock_module.GROUP_LABEL = "Collection"
        mock_module.PARENT_LABEL = "TokenSequence"
        self.training_data = data_prep_utils.TrainingData(None, mock_module)

    def test_xml(self):
        self.XMLequals(
            [("#", "foo"), ("1", "foo"), ("Pinto", "foo")],
            "<foo>#</foo> <foo>1</foo> <foo>Pinto</foo>",
        )
        self.XMLequals(
            [("&", "foo"), ("1", "foo"), ("Pinto", "foo")],
            "<foo>&amp;</foo> <foo>1</foo> <foo>Pinto</foo>",
        )

    def test_none_tag(self):
        self.XMLequals(
            [("Box", "foo"), ("#", "Null"), ("1", "foo"), ("Pinto", "foo")],
            "<foo>Box</foo> <Null>#</Null> <foo>1</foo> <foo>Pinto</foo>",
        )
        self.XMLequals(
            [("#", "Null"), ("1", "foo"), ("Pinto", "foo")],
            "<Null>#</Null> <foo>1</foo> <foo>Pinto</foo>",
        )

    def test_ampersand(self):
        assert self.training_data._xml_to_sequence(
            self.training_data._sequence_to_xml([("&", "foo")])
        ) == (("&", "foo"),)

    def XMLequals(self, labeled_sequence, xml):
        correct_xml = "<TokenSequence>" + xml + "</TokenSequence>"
        generated_xml = etree.tostring(
            self.training_data._sequence_to_xml(labeled_sequence)
        ).decode()
        print("Correct:   %s" % correct_xml)
        print("Generated: %s" % generated_xml)
        assert correct_xml == generated_xml


class TestTrainingDataIter(unittest.TestCase):
    def _td(self, xml_str):
        return data_prep_utils.TrainingData(xml=etree.fromstring(xml_str))

    def test_skips_comments(self):
        # Comments are useful for grouping examples in the same file; they
        # used to leak into __iter__ and crash trainModel.
        td = self._td(
            "<Collection>"
            "<!-- group one -->"
            "<TokenSequence><foo>a</foo></TokenSequence>"
            "<!-- group two -->"
            "<TokenSequence><foo>b</foo></TokenSequence>"
            "</Collection>"
        )
        assert [raw for raw, _ in td] == ["a", "b"]

    def test_skips_empty_sequences(self):
        td = self._td(
            "<Collection>"
            "<TokenSequence><foo>a</foo></TokenSequence>"
            "<TokenSequence></TokenSequence>"
            "<TokenSequence><foo>b</foo></TokenSequence>"
            "</Collection>"
        )
        assert [raw for raw, _ in td] == ["a", "b"]


if __name__ == "__main__":
    unittest.main()
