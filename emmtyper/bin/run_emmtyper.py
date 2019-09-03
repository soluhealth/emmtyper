"""
For running emmtyper
"""

import argparse
import pathlib
import os

from emmtyper.__init__ import __version__ as version
from emmtyper.__init__ import __name__ as name
from emmtyper.__init__ import __description__ as description
from emmtyper.__init__ import __epilog__ as epilog


from emmtyper.utilities import run_blast
from emmtyper.utilities import run_ispcr

DEFAULT_DB = pathlib.Path(__file__).parent.parent / "db" / "emm.fna"

class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    """
    Better formatting of argparse description and epilog, and include defaults.
    """

    pass


def build_parser():
    '''
    Parse command line arguments and options
    '''
    parser = argparse.ArgumentParser(
        prog=name,
        description="{} - Version {}".format(description, version),
        epilog=epilog,
        formatter_class=CustomFormatter,
    )

    subparsers = parser.add_subparsers(title="Approaches to choose from", metavar="")

    parser.add_argument(
        "--query", required=True, type=str, nargs="+", help="Genome(s) to PCR against."
    )
    parser.add_argument(
        "--db",
        required=True,
        type=str,
        help="The database to BLAST PCR product against.",
        default=os.environ.get("EMM_DB", DEFAULT_DB),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=version),
    )

    parser.add_argument(
        "-save",
        "--save_intermediary",
        default=False,
        action="store_true",
        help="Do not remove temporary isPcr and BLAST outputs.",
    )

    # Clusterer Options

    parser.add_argument(
        "-clust_distance",
        default=500,
        type=int,
        help="Distance in bp between clusters.",
    )
    parser.add_argument(
        "-output_type",
        nargs="?",
        type=str,
        default="short",
        choices=["short", "verbose", "visual"],
        help="Choose output type.",
    )
    parser.add_argument(
        "-output_file", default="stdout", type=str, help="File to stream final output."
    )

    # BLAST subparser
    parser_blast = subparsers.add_parser("blast", help="BLAST genomes against DB.")
    parser_blast = runBLAST.buildSubparser(parser_blast)
    parser_blast.set_defaults(func=runBLAST.main)

    # PCR + BLAST subparser

    parser_pcr = subparsers.add_parser(
        "pcr", help="Generate in silico PCR products, then BLAST against DB."
    )
    parser_pcr = runIsPCR.buildSubparser(parser_pcr)
    parser_pcr.set_defaults(func=runIsPCR.main)

    return parser


def main():
    '''
    Main function to parse command line arguments and options
    '''
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
