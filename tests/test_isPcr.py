import unittest

from emmail.objects.ispcr import IsPCR
from emmail.objects.blast import BLAST

from tests.data import *

ispcr = IsPCR(test_sequence_path, primer_path,
            min_perfect=15, min_good=15,
            max_product_length=4000,
            output_stream="stdout")

ispcr_e = IsPCR(test_empty_path, primer_path,
                min_perfect=20, min_good=30,
                max_product_length=4000,
                output_stream="stdout")
            
class testIsPCRapp(unittest.TestCase):

    def test_null(self):
        self.assertEqual(test_null, "this is a null test")
    
    def test_is_IsPCR(self):
        self.assertIs(type(ispcr), IsPCR)
        self.assertIs(type(ispcr_e), IsPCR)
    
    def test_isPcr_command(self):
        self.assertEqual(ispcr.build_isPCR_command(), isPcr_command)
    
    def test_isPcr_result(self):
        self.assertEqual(ispcr.run_isPCR(), isPcr_result)
    
    def test_empty_command(self):
        self.assertEqual(ispcr_e.build_isPCR_command(), isPcr_command_e)
    
    def test_empty_result(self):
        self.assertEqual(ispcr_e.run_isPCR(), isPcr_result_e)
    
    # How to test the connection between isPcr and BLAST?
    
if __name__ == '__main__':
    unittest.main()