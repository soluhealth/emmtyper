import unittest
from emmail.objects.Result import Result, WrongLengthException
from emmail.tests.test_data import *

row = Result(string)

class TestResultMethods(unittest.TestCase):
	
    def test_null(self):
        self.assertEqual(test_null, "this is a null test")
        
    def test_is_row(self):
        self.assertIs(type(row), Result)
        
    def test_raises_wrong_length(self):
        self.assertRaises(WrongLengthException, Result, string_long)
        
    def test_build_header(self):
        self.assertEqual(row.build_header(), header)

    def test_mismatch(self):
        self.assertTrue(row.mismatch_k(4))

    def test_align_diff(self):
        self.assertTrue(row.alignment_to_subject_length_k(5))
        
    def test_gap(self):
        self.assertTrue(row.gap_k(2))
        
    def test_filterMe(self):
        self.assertEqual(repr(row.filter(mismatch=4, align_diff=5, gap=2)), string)

if __name__ == '__main__':
    unittest.main()