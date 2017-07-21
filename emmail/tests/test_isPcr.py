from emmail.objects.IsPCR import IsPCR

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "contig.fasta"

primer_path = "isPcrPrim.tsv"

i = IsPCR.generateIsPCRobj(test_sequence_path, primer_path,
                        min_perfect=15, min_good=15,
                        min_product_length=0,
                        max_product_length=4000)

# print(i.build_isPcr_command())

print(i.run_isPcr_pipeline())