import unittest
import BlastResultObj

string = "a101\temm1\t100\t180\t0\t0\t1\t180\t180\t1\t1e5\t333\t180"		
row = BlastResultObj.Row(string)

class TestRowMethods(unittest.TestCase):
	def test_Query_IsString(self):
		self.assertIs(type(row.get_query()), str)
		
	def test_BlastHit_IsString(self):
		self.assertIs(type(row.get_blastHit()), str)
		
	def test_Mismatch_IsInteger(self):
		self.assertIs(type(row.get_mismatch()), str)
		
	def test_SubjectLength_IsInteger(self):
		self.assertIs(type(row.get_subjectLength()), int)




if __name__ == '__main__':
    unittest.main()