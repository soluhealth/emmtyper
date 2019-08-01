import unittest
from emmail.objects.resultRow import ResultRow, WrongLengthException
from emmail.tests.test_data import *

row = ResultRow(string)
row_not100 = ResultRow(string_not100)
row_imp = ResultRow(string_imp)

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
        
    def test_string_representation(self):
        self.assertEqual(str(row), string_str)
        self.assertEqual(str(row_not100), string_not100_str)
        self.assertEqual(str(row_imp), string_imp_str)

if __name__ == '__main__':
    unittest.main()