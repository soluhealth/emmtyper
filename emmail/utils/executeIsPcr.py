import argparse
import subprocess
import executeBlast

### SUPPORTING FUNCTIONS ###

def stderr_logic_filter(stderr):
    """
    Some stderr that we need not worry about.
    stderr within the list ignore_err will not be printed out.
    """
    ignore_err = [("FASTA-Reader: "
                    "Title ends with at least 20 valid nucleotide characters."
                    "  Was the sequence accidentally put in the title line?\n")]

    if stderr and stderr not in ignore_err:
        print(stderr)

### MAIN FUNCTIONS ###

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.add_argument("--genome", required=True,
                        help="The genome to PCR against.")
    parser.add_argument("--primer", required=True,
                        help="PCR primer. Text file with 3 columns: Name, Forward Primer, Reverse Primer.")
    parser.add_argument("--output", required=True,
                        help="Output filename, to use as BLAST query.")
    parser.add_argument("--db", required=True,
                        help="The database to BLAST PCR product against.")

    # isPcr options

    parser.add_argument("-maxSize", default=1500,
                        help="Maximum size of PCR product. Default is 1500.")

    # BLAST options

    parser.add_argument("-dust", default="no",
                        help="Filter query sequence with DUST. Default no.")
    parser.add_argument("-perc_identity", default=95,
                        help="Minimal percent identity of sequence. Default 95.")
    parser.add_argument("-culling_limit", default=1,
                        help="Total hits to return in a position. Default 1.")
    parser.add_argument("-outfmt", default="6 std slen",
                        help="Output format as in BLAST. Default \"6 std slen\".")
    parser.add_argument("-out", action="store",
                        help="File to stream output. Default to terminal.")

    parser.add_argument("-add_header", action="store_true", dest="header",
                        help="Add header to the output file on mention.")

    return parser

def runIsPcr(args):
    """
    Using args from argparse object, build a unix command to run isPcr.

    Input: args from argparse.argumentParser().
    Output: stdout and stderr of the subprocess run.
    """
    string = ("isPcr {0} {1} {2} -maxSize={3}")

    string = string.format(args.genome, args.primer, args.output, args.maxSize)

    process = subprocess.Popen(args=string, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    return process.communicate()

def runAll(args):
    stdout, stderr = runIsPcr(args)

    #stderr_logic_filter(stderr)

    args.query = args.output

    executeBlast.runAll(args)

    # subprocess.Popen(args=("rm {}".format(args.output)), shell=True)
