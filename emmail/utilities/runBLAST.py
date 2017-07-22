from emmail.objects.BLAST import BLAST

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
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
    parser.add_argument("-outBLAST", default=None, action="store",
                        help="File to stream output. Default to terminal.")

    return parser

def main(args):
    blast = BLAST(db = args.db, 
                    query = args.query, 
                    dust = args.dust, 
                    perc_identity = args.perc_identity,
                    culling_limit = args.culling_limit, 
                    outfmt = args.outfmt, 
                    out = args.outBLAST)
                    
    blast.run_blastn_pipeline()