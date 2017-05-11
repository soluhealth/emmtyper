import argparse
import subprocess
import filterBlastOutput

### SUPPORTING FUNCTIONS ###
def stderr_logic_filter(stderr):
    """
    Some stderr that we need not worry about.
    stderr within the list ignore_err will not be printed out.
    """
    ignore_err = [("FASTA-Reader: "
                    "Title ends with at least 20 valid nucleotide characters."
                    "  Was the sequence accidentally put in the title line?\n")]

    if stderr not in ignore_err:
        print(stderr)

def write_where(args, output):
    if args.out == None:
        print(output)
    else:
        if type(args.out) is str:
            out_conn = open(args.out, "w")
            out_conn.write(output)
            out_conn.close()

### MAIN FUNCTIONS ###

def buildSubparser(parser):
    # parser = argparse.ArgumentParser(description="Run Blastn from command line.")

    parser.add_argument("--db", required=True,
                        help="The database to BLAST against.")
    parser.add_argument("--query", required=True,
                        help="Query FASTA.")

    parser.add_argument("-makeblastDB", action="store_true", dest="makeDB",
                        help="Make blast db on directory on mention.")
    parser.add_argument("-add_header", action="store_true", dest="header",
                        help="Add header to the output file on mention.")
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

    return parser

def makeblastDB(args):
    """
    We might need to make a blastDB if the DB is not set up.
    """

    db_in = args.db
    db_name = db_in.split("/")[-1].split(".")[0]

    string = "makeblastdb -in {0} -dbtype {1} -title {2} -hash_index -out {2}"
    string = string.format(args.db, "nucl", db_name)

    subprocess.call(string)

def runBlast(args):
    """
    Using args from argparse object, build a unix command to run BLAST.

    Input: args from argparse.argumentParser().
    Output: stdout and stderr of the subprocess run.
    """
    string = ("blastn -db {0} -query {1} -dust {2} -perc_identity {3}"
                " -culling_limit {4} -outfmt {5}")

    string = string.format(args.db, args.query, args.dust,
                            args.perc_identity, args.culling_limit,
                            "\"{}\"".format(args.outfmt))

    process = subprocess.Popen(args=string, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    return process.communicate()

def run(args):
    # If user wants to make db, make one in working directory.
    # Assume no options change to makeblastdb.
    if args.makeDB == True:
        makeblastDB(args)
        args.db = args.db.split("/")[-1].split(".")[0]

    stdout, stderr = runBlast(args)

    # Divide BLAST output to lines, and process whether to print stderr or not.
    outputs = stdout.split("\n")[:-1]
    stderr_logic_filter(stderr)

    # Filter BLAST outputs and return.
    # Consider building options to filter outputs based on user intent.
    filtered_outputs = filterBlastOutput.filter(outputs, args.header)

    write_where(args, filtered_outputs)
    print("Finished! Thank you for using EmMAIL!")
