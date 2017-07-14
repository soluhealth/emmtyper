from Command import Command
from BLAST import BLAST

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/Pincer/TestData/contig.fasta"
test_assembly_path = "/home/andret1/dev/Pincer/TestData/LD_10702_6_10.fa"

assembly_1 = "/home/andret1/reads/genomes_test/LD_19944_5_36.fa"
assembly_2 = "/home/andret1/reads/genomes_test/LD_19944_5_65.fa"
assembly_3 = "/home/andret1/reads/genomes_test/LD_19944_6_145.fa"

b = BLAST.generateBLASTobj(db, assembly_2)

print(repr(b))
print(b.version)
b.run_blastn_pipeline()