'''
For running emmtyper
'''

import argparse

from emmtyper.__init__ import __version__ as version
from emmtyper.__init__ import __description__ as description
from emmtyper.__init__ import __author__ as author
from emmtyper.__init__ import __email__ as email
from emmtyper.__init__ import __name__ as name


from emmtyper.utilities import runBLAST
from emmtyper.utilities import runIsPCR

def build_parser():
    parser = argparse.ArgumentParser(prog=name,
                                    description="{} - Version {}".format(description, version),
                                    epilog="Developed by {} ({})".format(author, email))

    subparsers = parser.add_subparsers(title='Pipelines to choose from',
                                       metavar='')

    parser.add_argument("--query", required=True, type=str, nargs="+",
                        help="Genome(s) to PCR against.")
    parser.add_argument("--db", required=True, type=str,
                        help="The database to BLAST PCR product against.")

    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {version}'.format(version=version))

    parser.add_argument("-save", "--save_intermediary", default=False, action="store_true",
                    help="Temporary isPcr and BLAST outputs will not be removed on mention.")

    # Clusterer Options

    parser.add_argument("-clust_distance", default=500, type=int,
                        help="Distance between cluster to use. Default to cluster together within 500bp.")
    parser.add_argument("-output_type", nargs="?", type=str,
                        default="short", choices=["short", "verbose", "visual"],
                        help="Choose which output type is wanted. Default to short output.")
    parser.add_argument("-output_file", default="stdout", type=str,
                        help="File to stream final output. Default to terminal.")

    # BLAST subparser
    parser_blast = subparsers.add_parser("blast", help="Direct BLAST to genome reads.")
    parser_blast = runBLAST.buildSubparser(parser_blast)
    parser_blast.set_defaults(func=runBLAST.main)

    # PCR + BLAST subparser

    parser_pcr = subparsers.add_parser("pcr", help="PCR genome, then BLAST against it.")
    parser_pcr = runIsPCR.buildSubparser(parser_pcr)
    parser_pcr.set_defaults(func=runIsPCR.main)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
