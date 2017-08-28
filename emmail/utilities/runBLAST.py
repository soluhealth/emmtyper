from os import remove, environ
import logging

from emmail.objects.blast import BLAST

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.add_argument("--query", required=True, type=str,
                        help="Query FASTA.")
    parser.add_argument("--db", required=True, type=str,
                        help="The database to BLAST against.")
    
    
    parser.add_argument("-saveBLAST", default=False, action="store_true",
                        help="Temporary BLAST output will not be removed on mention.")
    #parser.add_argument("-add_header", default=False, action="store_true", 
                        #help="Add header to the output file on mention.")
    
    # BLAST Options
    
    parser.add_argument("-dust", default="no", type=str,
                        help="Filter query sequence with DUST. Default no.")
    parser.add_argument("-perc_identity", default=95, type=int,
                        help="Minimal percent identity of sequence. Default is 95.")
    parser.add_argument("-culling_limit", default=1, type=int,
                        help="Total hits to return in a position. Default is 1.")
    
    # ResultRow Options
    
    parser.add_argument("-mismatch", default=4, type=int,
                        help="Threshold for number of mismatch to allow in BLAST hit. Default is 4.")
    parser.add_argument("-align_diff", default=5, type=int,
                        help="Threshold for difference between alignment length and subject length in BLAST hit. Default is 5.")                        
    parser.add_argument("-gap", default=2, type=int,
                        help="Threshold gap to allow in BLAST hit. Default is 2.")
    
    # Clusterer Options
    
    parser.add_argument("-verbose", default=False, action="store_true",
                        help="Return verbose results instead of truncated result.")
    parser.add_argument("-outFinal", default="stdout", type=str,
                        help="File to stream final output. Default to terminal.")
    
    return parser

def main(args):
    outBLAST = args.query.split("/")[-1].split(".")[0] + ".tmp"
    
    blast = BLAST(db = args.db, 
                    query = args.query, 
                    dust = args.dust, 
                    perc_identity = args.perc_identity,
                    culling_limit = args.culling_limit, 
                    
                    output_stream = outBLAST,
                    header = False,
                    
                    mismatch = args.mismatch,
                    align_diff = args.align_diff,
                    gap = args.gap)
                    
    blast.run_blastn_pipeline()
    
    clusterer = Clusterer(blastOutputFile=outBLAST, 
                        output_stream=args.outFinal,
                        verbose=args.verbose).main()
                        
    if not args.saveBLAST:
        remove(outBLAST)
        # logger.info("{} is removed from directory".format(outBLAST))
        
    # logger.info("Result for {} is saved as {}".format(args.query.split("/")[-1], outBLAST))