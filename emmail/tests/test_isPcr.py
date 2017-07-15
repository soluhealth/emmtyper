from IsPCR import IsPCR

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "/home/andret1/dev/Pincer/TestData/contig.fasta"

primer_path = "/home/andret1/dev/EmMAIL/emmail/test/isPcrPrim.tsv"

i = IsPCR.generateIsPCRobj(test_sequence_path, primer_path)

print(i.build_isPcr_command())

print(i.run_isPcr_pipeline())