from emmail.objects.IsPCR import IsPCR
from emmail.objects.BLAST import BLAST

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.add_argument("--genome", required=True,
                        help="The genome to PCR against.")
    parser.add_argument("--primer", required=True,
                        help="PCR primer. Text file with 3 columns: Name, Forward Primer, Reverse Primer.")
    parser.add_argument("--db", required=True,
                        help="The database to BLAST PCR product against.")

    # isPcr options
    
    parser.add_argument("-outPCR", default="pcr.tmp",
                        help="Output filename, to use as BLAST query. Default to pcr.tmp.")
    parser.add_argument("-minPerfect", default=15,
                        help="Minimum size of perfect match at 3' primer end. Default is 15.")
    parser.add_argument("-minGood", default=15,
                        help=("Minimum size where there must be 2 matches for each mismatch."
                              "Default is 15; there must be 10 match in 15bp primer size."))
    parser.add_argument("-minSize", default=0,
                        help="Minimum size of PCR product. Default is 0.")
    parser.add_argument("-maxSize", default=4000,
                        help="Maximum size of PCR product. Default is 4000.")

    # BLAST options

    parser.add_argument("-dust", default="no",
                        help="Filter query sequence with DUST. Default no.")
    parser.add_argument("-perc_identity", default=95,
                        help="Minimal percent identity of sequence. Default 95.")
    parser.add_argument("-culling_limit", default=1,
                        help="Total hits to return in a position. Default 1.")
    parser.add_argument("-outfmt", default="6 std slen",
                        help="Output format as in BLAST. Default \"6 std slen\".")
    parser.add_argument("-outBLAST", default=None, action="store",
                        help="File to stream BLAST output. Default to terminal.")

    #parser.add_argument("-add_header", action="store_true", dest="header",
                        #help="Add header to the output file on mention.")

    return parser
    
def main(args):
    pcr = IsPCR(assembly_filename = args.genome,
                primer_filename = args.primer,
                min_perfect = args.minPerfect,
                min_good = args.minGood,
                min_product_length = args.minSize,
                max_product_length = args.maxSize,
                output_stream = args.outPCR)
    
    pcr.run_isPCR()
    
    args.query = args.outPCR
    
    blast = BLAST(db = args.db, 
                    query = args.query, 
                    dust = args.dust, 
                    perc_identity = args.perc_identity,
                    culling_limit = args.culling_limit, 
                    outfmt = args.outfmt, 
                    out = args.outBLAST)
                    
    blast.run_blastn_pipeline()