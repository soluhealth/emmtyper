import argparse
import subprocess
import utils.executeBlast as executeBlast

def buildParser():
    parser = argparse.ArgumentParser(description="EmMAIL - emm Automatic Isolate Labeler")
    subparsers = parser.add_subparsers(title='Pipelines to choose from',
                                       metavar='')

    # BLAST subparser
    parser_blast = subparsers.add_parser("blast", help="Direct BLAST to genome reads.")
    parser_blast = executeBlast.buildSubparser(parser_blast)
    parser_blast.set_defaults(func=executeBlast.run)

    # PCR + BLAST subparser
    parser_pcr = subparsers.add_parser("pcr", help="PCR genome, then BLAST against it.")

    return parser

def main():
    parser = buildParser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
