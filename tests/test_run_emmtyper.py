"""
Test the command line intereface
"""

from click.testing import CliRunner
from emmtyper.bin.run_emmtyper import main
from emmtyper import __version__ as version

from tests.data import test_sequence_path


runner = CliRunner()


def test_run_emmtyper_version():
    """
    Test emmtyper --version flag
    """
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"emmtyper v{version}\n"


def test_run_emmtyper_basic_blast():
    """
    Test basic blast workflow
    """
    result = runner.invoke(main, [test_sequence_path])
    assert result.exit_code == 0
    assert result.output == "contig.tmp\t1\tEMM1.0\t\tA-C3\n"


def test_run_emmtyper_basic_ispcr():
    """
    Test basic ispcr workflow
    """
    result = runner.invoke(main, ["-w", "pcr", test_sequence_path])
    assert result.exit_code == 0
    assert result.output == "contig_pcr.tmp\t1\tEMM1.0\t\tA-C3\n"
