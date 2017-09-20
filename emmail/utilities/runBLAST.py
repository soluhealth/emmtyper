from os import remove, environ
import logging

from emmail.objects.blast import BLAST
from emmail.objects.clusterer import Clusterer

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.usage = "emmail --db <DB> --query <QUERY> [OPTIONS] blast [OPTIONS]"

    # BLAST options

    parser.add_argument("-dust", default="no", type=str,
                        help="Filter query sequence with DUST. Default no.")
    parser.add_argument("-perc_identity", default=95, type=int,
                        help="Minimal percent identity of sequence. Default is 95.")
    parser.add_argument("-culling_limit", default=5, type=int,
                        help="Total hits to return in a position. Default is 5.")

    # ResultRow options
    
    parser.add_argument("-mismatch", default=4, type=int,
                        help="Threshold for number of mismatch to allow in BLAST hit. Default is 4.")
    parser.add_argument("-align_diff", default=5, type=int,
                        help="Threshold for difference between alignment length and subject length in BLAST hit. Default is 5.")                        
    parser.add_argument("-gap", default=2, type=int,
                        help="Threshold gap to allow in BLAST hit. Default is 2.")
    
    return parser

def main(args):
    for query in args.query:
    
        outBLAST = query.split("/")[-1].split(".")[0] + ".tmp"

        blast = BLAST(db = args.db, 
                        query = query, 
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
                            distance = args.clust_distance,
                            output_stream=args.outFinal,
                            verbose=args.verbose).main()
                            
        if not args.saveIntermediary:
            remove(outBLAST)
            # logger.info("{} is removed from directory".format(outBLAST))
            
        # logger.info("Result for {} is saved as {}".format(args.query.split("/")[-1], outBLAST))