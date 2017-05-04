from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description="Utility script to build reference file based on used MLST database")

parser.add_argument("--inputDB", required=True, help="MLST database")
parser.add_argument("--filetype", default="fasta", help="Type of file of the MLST database")
parser.add_argument("--output", required=True, help="Name of txt file where reference should be")

args = parser.parse_args()

input_file = open(args.inputDB, "r")
new_file = open(args.output, "w")

fasta_sequences = SeqIO.parse(input_file, args.filetype)

new_file.write("{}\t{}\n".format("ST", "emm"))

for fasta in fasta_sequences:
    new_file.write("{}\t{}\n".format(fasta.id, fasta.id))

input_file.close()
new_file.close()

print "Finished making reference file as {}".format(args.output)

