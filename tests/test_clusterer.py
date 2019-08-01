import unittest

from emmtyper.objects.clusterer import Clusterer
from tests.data import *

# Single BLAST output file

clusterer = Clusterer(blastOutputFile=test_blast_product, 
                        output_stream="stdout",
                        output_type="short",
                        header=False,
                        distance=800)

clusterer_verbose = Clusterer(blastOutputFile=test_blast_product, 
                        output_stream="stdout",
                        output_type="verbose",
                        header=True,
                        distance=800)                        
                        
class testClusterer(unittest.TestCase):

    def test_null(self):
        self.assertEqual(test_null, "this is a null test")

    def test_is_clusterer(self):
        self.assertIs(type(clusterer), Clusterer)
        self.assertIs(type(clusterer_verbose), Clusterer)
    
    def test_repr_short(self):
        self.assertEqual(repr(clusterer), clusterer_repr_short)
        self.assertEqual(repr(clusterer_verbose), clusterer_repr_verbose)
        
    def test_run_short(self):
        self.assertEqual(clusterer.main(), clusterer_result_short)
        
    def test_run_verbose(self):
        self.assertEqual(clusterer_verbose.main(), clusterer_result_verbose)
        
if __name__ == "__main__":
    unittest.main()