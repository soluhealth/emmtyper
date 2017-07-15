from Command import Command
from BLAST import BLAST

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/Pincer/TestData/contig.fasta"

b = BLAST.generateBLASTobj(db, assembly_2)

print(repr(b))
print(b.version)
b.run_blastn_pipeline()