from emmail.objects.BLAST import BLAST

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    # parser = argparse.ArgumentParser(description="Run Blastn from command line.")

    parser.add_argument("--db", required=True,
                        help="The database to BLAST against.")
    parser.add_argument("--query", required=True,
                        help="Query FASTA.")

    #parser.add_argument("-add_header", action="store_true", dest="header",
                        #help="Add header to the output file on mention.")
                        
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

def main(args):
    blast = BLAST(args.db, args.query, 
                    args.dust, args.perc_identity,
                    args.culling_limit, 
                    args.outfmt, args.out)
                    
    blast.run_blastn_pipeline()