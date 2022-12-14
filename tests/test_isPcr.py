import unittest

from emmtyper.objects.ispcr import IsPCR

from tests.data import primer_path_cdc, \
                       primer_path_frost, \
                        test_sequence_path, \
                        test_empty_path, \
                        test_null, \
                        isPcr_command_cdc, \
                        isPcr_command_e_cdc, \
                        isPcr_command_frost, \
                        isPcr_command_e_frost, \
                        isPcr_result_cdc, \
                        isPcr_result_frost, \
                        isPcr_result_e \

ispcr_cdc = IsPCR(
    test_sequence_path,
    primer_path_cdc,
    min_perfect=15,
    min_good=15,
    #tile_size=6,
    #step_size=5,
    max_product_length=4000,
    tile_size=6,
    step_size=5,
    output_stream="stdout",
)

ispcr_frost = IsPCR(
    test_sequence_path,
    primer_path_frost,
    min_perfect=15,
    min_good=15,
    #tile_size=6,
    #step_size=5,
    max_product_length=4000,
    tile_size=6,
    step_size=5,
    output_stream="stdout",
)


ispcr_e_cdc = IsPCR(
    test_empty_path,
    primer_path_cdc,
    min_perfect=20,
    min_good=30,
    #tile_size=6,
    #step_size=5,
    max_product_length=4000,
    tile_size=6,
    step_size=5,
    output_stream="stdout",
)


ispcr_e_frost = IsPCR(
    test_empty_path,
    primer_path_frost,
    min_perfect=20,
    min_good=30,
    #tile_size=6,
    #step_size=5,
    max_product_length=4000,
    tile_size=6,
    step_size=5,
    output_stream="stdout",
)


class testIsPCRapp(unittest.TestCase):
    def test_null(self):
        self.assertEqual(test_null, "this is a null test")

    def test_is_IsPCR(self):
        self.assertIs(type(ispcr_cdc), IsPCR)
        self.assertIs(type(ispcr_e_cdc), IsPCR)
        self.assertIs(type(ispcr_frost), IsPCR)
        self.assertIs(type(ispcr_e_frost), IsPCR)

    '''def test_isPcr_command(self):
        self.assertTrue(isPcr_command_cdc in ispcr_cdc.build_isPCR_command())
        self.assertTrue(isPcr_command_frost in ispcr_frost.build_isPCR_command())

    def test_isPcr_result(self):
        self.assertEqual(ispcr_cdc.run_isPCR(), isPcr_result_cdc)
        self.assertEqual(ispcr_frost.run_isPCR(), isPcr_result_frost)

    def test_empty_command(self):
        self.assertTrue(isPcr_command_e_cdc in ispcr_e_cdc.build_isPCR_command())
        self.assertTrue(isPcr_command_e_frost in ispcr_e_frost.build_isPCR_command())'''

    def test_empty_result(self):
        self.assertEqual(ispcr_e_cdc.run_isPCR(), isPcr_result_e)
        self.assertEqual(ispcr_e_frost.run_isPCR(), isPcr_result_e)

    # How to test the connection between isPcr and BLAST?


if __name__ == "__main__":
    unittest.main()
