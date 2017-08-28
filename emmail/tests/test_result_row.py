import unittest
from emmail.objects.resultRow import ResultRow, WrongLengthException
from emmail.tests.test_data import *

row = ResultRow(string)

class TestResultMethods(unittest.TestCase):
	
    def test_null(self):
        self.assertEqual(test_null, "this is a null test")
        
    def test_is_row(self):
        self.assertIs(type(row), ResultRow)
        
    def test_raises_wrong_length(self):
        self.assertRaises(WrongLengthException, ResultRow, string_long)
        
    def test_build_header(self):
        self.assertEqual(row.build_header(), header)

    def test_mismatch(self):
        self.assertTrue(row.mismatch_k(4))

    def test_align_diff(self):
        self.assertTrue(row.alignment_to_subject_length_k(5))
        
    def test_gap(self):
        self.assertTrue(row.gap_k(2))
        
    def test_filter_me(self):
        self.assertTrue(row.filter(mismatch=4, align_diff=5, gap=2))

if __name__ == '__main__':
    unittest.main()