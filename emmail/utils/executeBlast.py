from Bio.Blast.Applications import NcbiblastnCommandline
import argparse
import os

def buildParser():
    parser = argparse.ArgumentParser(description="Python script to run Blastn from command line.")

    parser.add_argument("-makeblastDB", action="store_true", dest="makeDB", help="Will make blast db on working directory if mentioned.")
    
    parser.add_argument("--db", required=True, help="The database to BLAST against.")
    parser.add_argument("--query", required=True, help="Query FASTA.")
    parser.add_argument("-dust", default="no", help="Filter query sequence with DUST, as defined in BLAST. Default no.")
    parser.add_argument("-perc_identity", default=95, help="Minimal percent identity, as in BLAST. Default 95.")
    parser.add_argument("-culling_limit", default=1, help="Number of hits to return in a single position, as in BLAST. Default 1.")
    parser.add_argument("-outfmt", default="6 std slen", help="Intended output format, as in BLAST. Default \"6 std slen\".")
    parser.add_argument("-out", default="-", help="File output, as in BLAST. Default output to terminal.")
    
    return parser

def makeblastDB(args):
    """
    We might need to make a blastDB if the DB is not set up.
    """
    
    db_in = args.db
    db_name = db_in.split("/")[-1].split(".")[0]
    
    string = "makeblastdb -in {0} -dbtype {1} -title {2} -hash_index -out {2}"
    string = string.format(args.db, "nucl", db_name)
    
    print(string)
    # os.system(string)

def runBlast(args):
    string = "blastn -db {0} -query {1} -dust {2} -perc_identity {3} -culling_limit {4} -outfmt {5} -out {6}"
    
    string = string.format(args.db, args.query, args.dust, args.perc_identity, 
                           args.culling_limit, "\"{}\"".format(args.outfmt), args.out)
    
    print(string)
    # os.system(string)

parser = buildParser()
args = parser.parse_args()

if args.makeDB == True:
    makeblastDB(args)
    args.db = args.db.split("/")[-1].split(".")[0]

runBlast(args)