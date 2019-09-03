'''
Define the workflow to run PCR using isPcr
'''
from os import remove, environ
import logging
import pathlib

from emmtyper.objects.ispcr import IsPCR
from emmtyper.objects.blast import BLAST
from emmtyper.objects.clusterer import Clusterer

from emmtyper.utilities import *

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

DEFAULT_PRIMERS = pathlib.Path(__file__).parent.parent / "data" / "isPcrPrim.tsv"

def buildSubparser(parser):
    """
    Add arguments to the subparser, and return the subparser.
    """
    parser.usage = (
        "emmtyper --query <QUERY> --db <DB> [OPTIONS] pcr --primer <PRIMER> [OPTIONS]"
    )

    parser.add_argument(
        "--primer",
        required=True,
        type=str,
        help="PCR primer. Text file with 3 columns: Name, Forward Primer, Reverse Primer.",
        default = environ.get("EMM_PCR", DEFAULT_PRIMERS)
    )

    # isPcr options

    parser.add_argument(
        "-minPerfect",
        default=minPerfect_default,
        type=int,
        help="Minimum size of perfect match at 3' primer end. Default is {}.".format(
            minPerfect_default
        ),
    )
    parser.add_argument(
        "-minGood",
        default=minGood_default,
        type=int,
        help=(
            "Minimum size where there must be 2 matches for each mismatch. "
            "Default is {0}; there must be {1} match in {0}bases primer size."
        ).format(minGood_default, int(0.67 * minGood_default)),
    )
    parser.add_argument(
        "-maxSize",
        default=maxSize_default,
        type=int,
        help="Maximum size of PCR product. Default is {}.".format(maxSize_default),
    )

    # BLAST options

    parser.add_argument(
        "-dust",
        default="no",
        type=str,
        help="Filter query sequence with DUST. Default no.",
    )
    parser.add_argument(
        "-perc_identity",
        default=perc_id_default,
        type=int,
        help="Minimal percent identity of sequence. Default is {}.".format(
            perc_id_default
        ),
    )
    parser.add_argument(
        "-culling_limit",
        default=culling_default,
        type=int,
        help="Total hits to return in a position. Default is 5.".format(
            culling_default
        ),
    )

    # ResultRow options

    parser.add_argument(
        "-mismatch",
        default=mismatch_default,
        type=int,
        help="Threshold for number of mismatch to allow in BLAST hit. Default is {}.".format(
            mismatch_default
        ),
    )
    parser.add_argument(
        "-align_diff",
        default=align_diff_default,
        type=int,
        help="Threshold for difference between alignment length and subject length in BLAST hit. Default is {}.".format(
            align_diff_default
        ),
    )
    parser.add_argument(
        "-gap",
        default=gap_default,
        type=int,
        help="Threshold gap to allow in BLAST hit. Default is {}.".format(gap_default),
    )

    parser.add_argument(
        "--blast_path",
        default=None,
        type=str,
        help="Specify full path to blastn executable. Otherwise search $PATH."
    )

    parser.add_argument(
        "--ispacr_path",
        default=None,
        type=str,
        help="Specify full path to isPcr executable. Otherwise search $PATH."
    )

    return parser


def main(args):
    logger.info("Start running emmtyper on {} queries.".format(len(args.query)))

    for i, query in enumerate(args.query):

        outPCR = query.split("/")[-1].split(".")[0] + "_pcr.tmp"
        outBLAST = query.split("/")[-1].split(".")[0] + ".tmp"

        pcr = IsPCR(
            assembly_filename=query,
            primer_filename=args.primer,
            min_perfect=args.minPerfect,
            min_good=args.minGood,
            max_product_length=args.maxSize,
            output_stream="stdout",
            tool_path=args.ispcr_path,
        )

        # Run isPcr, take output and use it as input for Blast.
        with open(outPCR, "w") as temp:
            temp.write(pcr.run_isPCR())

        blast = BLAST(
            db=args.db,
            query=outPCR,
            dust=args.dust,
            perc_identity=args.perc_identity,
            culling_limit=args.culling_limit,
            output_stream=outBLAST,
            header=False,
            mismatch=args.mismatch,
            align_diff=args.align_diff,
            gap=args.gap,
            tool_path=args.tool_path,
        )

        blast.run_blastn_pipeline()

        clusterer = Clusterer(
            blastOutputFile=outBLAST,
            distance=args.clust_distance,
            output_stream=args.output_file,
            output_type=args.output_type,
        ).main()

        if not args.save_intermediary:
            remove(outPCR)
            remove(outBLAST)
            # logger.info("{} and {} are removed from directory".format(args.outPCR))

    logger.info("Finished emmtyper.")
