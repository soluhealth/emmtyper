import unittest
from emmail.objects.BLAST import BLAST

test_no_path = "this is a null test"

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/EmMAIL/emmail/tests/contig.fasta"

test_command = "blastn -db {} -query {} -dust no -perc_identity 95 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)
test_command_h = "blastn -db {} -query {} -dust no -perc_identity 100 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)

test_header = "Query\tBlastHit\tIdentity\tAlignmentLength\tMismatch\tGapOpen\tQueryStart\tQueryEnd\tHitStart\tHitEnd\tE-Value\tBitScore\tSubjectLength\n"
test_result = "contig1\tEMM1.0\t100.000\t180\t0\t0\t113816\t113995\t1\t180\t1.30e-90\t333\t180"

b = BLAST(db, test_sequence_path, dust="no",
          perc_identity=95, culling_limit=1,
          output_stream=None, header=False,
          mismatch=4, align_diff=5, gap=2)

b_header = BLAST(db, test_sequence_path, dust="no",
          perc_identity=100, culling_limit=1,
          output_stream=None, header=True,
          mismatch=4, align_diff=5, gap=2)

class testBLASTapp(unittest.TestCase):
    
    def test_null(self):
        self.assertEqual(test_no_path, "this is a null test")
        
    def test_is_BLAST(self):
        self.assertIs(type(b), BLAST)
        self.assertIs(type(b_header), BLAST)
        
    def test_b_repr(self):
        self.assertEqual(repr(b), test_command)
        
    def test_b_command(self):
        self.assertEqual(b.build_blastn_command(), test_command)
    
    def test_b_header_command(self):
        self.assertEqual(b_header.build_blastn_command(), test_command_h)
    
    def test_b_out(self):
        self.assertEqual(b.run_blastn_pipeline(), test_result)
        
    def test_b_header_out(self):
        self.assertEqual(b_header.run_blastn_pipeline(), test_header+test_result)
        
if __name__ == '__main__':
    unittest.main()       