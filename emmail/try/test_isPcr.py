from IsPCR import IsPCR

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/Pincer/TestData/contig.fasta"
test_assembly_path = "/home/andret1/dev/Pincer/TestData/LD_10702_6_10.fa"

primer_path = "/home/andret1/dev/Pincer/TestData/isPcrPrim.tsv"

assembly_1 = "/home/andret1/reads/genomes_test/LD_19944_5_36.fa"
assembly_2 = "/home/andret1/reads/genomes_test/LD_19944_5_65.fa"
assembly_3 = "/home/andret1/reads/genomes_test/LD_19944_6_145.fa"

i = IsPCR.generateIsPCRobj(test_sequence_path, primer_path)

print(i.build_isPcr_command())

print(i.run_isPcr_pipeline())