from emmail.objects.BLAST import BLAST

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.add_argument("--db", required=True, type=str,
                        help="The database to BLAST against.")
    parser.add_argument("--query", required=True, type=str,
                        help="Query FASTA.")

    parser.add_argument("-dust", default="no", type=str,
                        help="Filter query sequence with DUST. Default no.")
    parser.add_argument("-perc_identity", default=95, type=int,
                        help="Minimal percent identity of sequence. Default 95.")
    parser.add_argument("-culling_limit", default=1, type=int,
                        help="Total hits to return in a position. Default 1.")
    parser.add_argument("-outBLAST", default="None", 
                        action="store", type=str,
                        help="File to stream output. Default to terminal.")

    parser.add_argument("-add_header", default=False, action="store_true", 
                        help="Add header to the output file on mention.")
                        
    return parser

def main(args):
    blast = BLAST(db = args.db, 
                    query = args.query, 
                    dust = args.dust, 
                    perc_identity = args.perc_identity,
                    culling_limit = args.culling_limit, 
                    
                    out = args.outBLAST,
                    header = args.add_header)
                    
    blast.run_blastn_pipeline()