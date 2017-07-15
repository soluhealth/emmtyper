import unittest
import BlastResultObj

string = "SP3LAU\tEMM89.0\t100\t180\t0\t0\t737626\t737805\t1\t180\t1.93e-89\t333\t180"	
row = BlastResultObj.Row(string)

class TestRowMethods(unittest.TestCase):
	
	def test_mismatch(self):
		self.assertTrue(row.mismatch_k(4))
	
	def test_align_diff(self):
		self.assertTrue(row.alignment_to_subject_length_k(5))
		
	def test_gap(self):
		self.assertTrue(row.gap_k(2))
		
	def test_filterMe(self):
		self.assertIs(row.filterMe(), string)

if __name__ == '__main__':
    unittest.main()