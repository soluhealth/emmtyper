import unittest

from emmtyper.objects.blast import BLAST
from tests.data import test_sequence_path, db, \
                       test_empty_path, blast_command, \
                        blast_command_h, blast_result, \
                        test_null, header

# Normal no nonsense BLAST.
blast = BLAST(
    db,
    test_sequence_path,
    dust="no",
    perc_identity=95,
    culling_limit=1,
    output_stream=None,
    header=False,
    mismatch=4,
    align_diff=5,
    gap=2,
    tool_path=None,
)

# BLAST result with header.
blast_h = BLAST(
    db,
    test_sequence_path,
    dust="no",
    perc_identity=100,
    culling_limit=1,
    output_stream=None,
    header=True,
    mismatch=4,
    align_diff=5,
    gap=2,
    tool_path=None,
)

# BLAST result will be empty.
blast_e = BLAST(
    db,
    test_empty_path,
    dust="no",
    perc_identity=100,
    culling_limit=1,
    output_stream=None,
    header=True,
    mismatch=0,
    align_diff=0,
    gap=0,
    tool_path=None,
)


class testBLASTapp(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(test_null, "this is a null test")

    def test_is_BLAST(self):
        self.assertIs(type(blast), BLAST)
        self.assertIs(type(blast_h), BLAST)

    def test_b_repr(self):
        self.assertTrue(blast_command in repr(blast))

    def test_b_command(self):
        self.assertTrue(blast_command in blast.build_blastn_command())

    def test_b_out(self):
        self.assertEqual(blast.run_blastn_pipeline(), blast_result)

    def test_h_command(self):
        self.assertTrue(blast_command_h in blast_h.build_blastn_command())

    def test_h_out(self):
        self.assertEqual(blast_h.run_blastn_pipeline(), header + blast_result)

    def test_e_out(self):
        self.assertEqual(blast_e.run_blastn_pipeline(), "")


if __name__ == "__main__":
    unittest.main()
