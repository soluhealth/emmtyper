import unittest
from emmail.objects.IsPCR import IsPCR

test_no_path = "this is a null test"

primer_path = "/home/andret1/dev/EmMAIL/emmail/tests/isPcrPrim.tsv"
db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/EmMAIL/emmail/tests/contig.fasta"

test_command = "blastn -db {} -query {} -dust no -perc_identity 95 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)
test_command_h = "blastn -db {} -query {} -dust no -perc_identity 100 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)

test_header = "Query\tBlastHit\tIdentity\tAlignmentLength\tMismatch\tGapOpen\tQueryStart\tQueryEnd\tHitStart\tHitEnd\tE-Value\tBitScore\tSubjectLength\n"
test_result = "contig1\tEMM1.0\t100.000\t180\t0\t0\t113816\t113995\t1\t180\t1.30e-90\t333\t180"

isPcr_command = "isPcr {} {} stdout -minPerfect=15 -minGood=15 -maxSize=4000".format(test_sequence_path, primer_path)
isPcr_result = ">contig1:113750+114924 emm 1175bp TATTCGCTTAGAAAATTAA GCAAGTTCTTCAGCTTGTTT\nTATTCGCTTAGAAAATTAAaaacaggaacggcttcagtagcggtagcttt\ngactgttttaggggcaggttttgcgaatcaaacagaggttaaggctaacg\ngtgatggtaatcctagggaagttatagaagatcttgcagcaaacaatccc\ngcaatacaaaatatacgtttacgtcacgaaaacaaggacttaaaagcgag\nattagagaatgcaatggaagttgcaggaagagattttaagagagctgaag\naacttgaaaaagcaaaacaagccttagaagaccagcgtaaagatttagaa\nactaaattaaaagaactacaacaagactatgacttagcaaaggaatcaac\naagttgggatagacaaagacttgaaaaagagttagaagagaaaaaggaag\nctcttgaattagcgatagaccaggcaagtcgggactaccatagagctacc\ngctttagaaaaagagttagaagagaaaaagaaagctcttgaattagcgat\nagaccaagcgagtcaggactataatagagctaacgtcttagaaaaagagt\ntagaaacgattactagagaacaagagattaatcgtaatcttttaggcaat\ngcaaaacttgaacttgatcaactttcatctgaaaaagagcagctaacgat\ncgaaaaagcaaaacttgaggaagaaaaacaaatctcagacgcaagtcgtc\naaagccttcgtcgtgacttggacgcatcacgtgaagctaagaaacaggtt\ngaaaaagatttagcaaacttgactgctgaacttgataaggttaaagaaga\ncaaacaaatctcagacgcaagccgtcaaggccttcgccgtgacttggacg\ncatcacgtgaagctaagaaacaggttgaaaaagatttagcaaacttgact\ngctgaacttgataaggttaaagaagaaaaacaaatctcagacgcaagccg\ntcaaggccttcgccgtgacttggacgcatcacgtgaagctaagaaacaag\nttgaaaaagctttagaagaagcaaacagcaaattagctgctcttgaaaaa\ncttaacaaagagcttgaagaaagcaagaaattaacagaaaaagaaaaagc\ntgaactacaagcaaaacttgaagcagaagcaaaagcactcaaagaacaat\ntagcgAAACAAGCTGAAGAACTcGC"

i = IsPCR(test_sequence_path, primer_path,
            min_perfect=15, min_good=15,
            min_product_length=0,
            max_product_length=4000,
            output_stream="stdout")

class testIsPCRapp(unittest.TestCase):

    def test_null(self):
        self.assertEqual(test_no_path, "this is a null test")
    
    def test_is_IsPCR(self):
        self.assertIs(type(i), IsPCR)
    
    def test_isPcr_command(self):
        self.assertEqual(i.build_isPCR_command(), isPcr_command)
    
    def test_isPcr_result(self):
        self.assertEqual(i.run_isPCR(), isPcr_result)
        
    # How to connect to blastn?
        
if __name__ == '__main__':
    unittest.main()  