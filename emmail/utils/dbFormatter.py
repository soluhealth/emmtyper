from Bio import SeqIO
import argparse

# Build parser and parse args

parser = argparse.ArgumentParser(description="Utility script to build reference file based on used MLST database")

parser.add_argument("--inputDB", required=True, help="MLST database")
parser.add_argument("--filetype", default="fasta", help="Type of file of the MLST database")
parser.add_argument("--outputDB", required=True, help="Name of fasta file where reference db should be")
parser.add_argument("--outputRef", required=True, help="Name of txt file where reference should be")

args = parser.parse_args()

# Open files

input_file = open(args.inputDB, "r")

new_db = open(args.outputDB, "w")
new_ref = open(args.outputRef, "w")

fasta_sequences = SeqIO.parse(input_file, args.filetype)

# Make MLST DB fasta

print "Starting building MLST DB"

for fasta in SeqIO.parse(open(args.inputDB, "r"), args.filetype):
    new_db.write(">{}-{}\n{}\n".format(fasta.id[0:3],fasta.id, fasta.seq))

print "Finished building MLST DB"

# Make MLST reference txt

print "Starting building MLST reference"

new_ref.write("{}\t{}\n".format("ST", "emm"))

for fasta in SeqIO.parse(open(args.inputDB, "r"), args.filetype):
    new_ref.write("{}\t{}\n".format(fasta.id, fasta.id))
    
print "Finished building MLST reference"

# Close all

input_file.close()
new_db.close()
new_ref.close()

print "Your new files are shown as:\nDB: {}\nReference: {}\n".format(args.outputDB, args.outputRef)
print "Thank you for using dbFormatter."

