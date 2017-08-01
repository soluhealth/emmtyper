test_null = "this is a null test"

primer_path = "/home/andret1/dev/EmMAIL/emmail/tests/isPcrPrim.tsv"
db = "/home/andret1/projects/blastDB/8Jun17.fasta"

test_sequence_path = "/home/andret1/dev/EmMAIL/emmail/tests/contig.fasta"
test_empty_path = "/home/andret1/dev/EmMAIL/emmail/tests/no.fasta"
test_pcr_product_path = "/home/andret1/dev/EmMAIL/emmail/tests/amplicon.fasta"

blast_command = "blastn -db {} -query {} -dust no -perc_identity 95 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)
blast_command_h = "blastn -db {} -query {} -dust no -perc_identity 100 -culling_limit 1 -outfmt \"6 std slen\"".format(db, test_sequence_path)
isPcr_command = "isPcr {} {} stdout -minPerfect=15 -minGood=15 -maxSize=4000".format(test_sequence_path, primer_path)
isPcr_command_e = "isPcr {} {} stdout -minPerfect=20 -minGood=30 -maxSize=4000".format(test_empty_path, primer_path)

blast_header = "Query\tBlastHit\tIdentity\tAlignmentLength\tMismatch\tGapOpen\tQueryStart\tQueryEnd\tHitStart\tHitEnd\tE-Value\tBitScore\tSubjectLength\n"
blast_result = "contig1\tEMM1.0\t100.000\t180\t0\t0\t113816\t113995\t1\t180\t1.30e-90\t333\t180"

isPcr_result = ">contig1:113750+114924 emm 1175bp TATTCGCTTAGAAAATTAA GCAAGTTCTTCAGCTTGTTT\nTATTCGCTTAGAAAATTAAaaacaggaacggcttcagtagcggtagcttt\ngactgttttaggggcaggttttgcgaatcaaacagaggttaaggctaacg\ngtgatggtaatcctagggaagttatagaagatcttgcagcaaacaatccc\ngcaatacaaaatatacgtttacgtcacgaaaacaaggacttaaaagcgag\nattagagaatgcaatggaagttgcaggaagagattttaagagagctgaag\naacttgaaaaagcaaaacaagccttagaagaccagcgtaaagatttagaa\nactaaattaaaagaactacaacaagactatgacttagcaaaggaatcaac\naagttgggatagacaaagacttgaaaaagagttagaagagaaaaaggaag\nctcttgaattagcgatagaccaggcaagtcgggactaccatagagctacc\ngctttagaaaaagagttagaagagaaaaagaaagctcttgaattagcgat\nagaccaagcgagtcaggactataatagagctaacgtcttagaaaaagagt\ntagaaacgattactagagaacaagagattaatcgtaatcttttaggcaat\ngcaaaacttgaacttgatcaactttcatctgaaaaagagcagctaacgat\ncgaaaaagcaaaacttgaggaagaaaaacaaatctcagacgcaagtcgtc\naaagccttcgtcgtgacttggacgcatcacgtgaagctaagaaacaggtt\ngaaaaagatttagcaaacttgactgctgaacttgataaggttaaagaaga\ncaaacaaatctcagacgcaagccgtcaaggccttcgccgtgacttggacg\ncatcacgtgaagctaagaaacaggttgaaaaagatttagcaaacttgact\ngctgaacttgataaggttaaagaagaaaaacaaatctcagacgcaagccg\ntcaaggccttcgccgtgacttggacgcatcacgtgaagctaagaaacaag\nttgaaaaagctttagaagaagcaaacagcaaattagctgctcttgaaaaa\ncttaacaaagagcttgaagaaagcaagaaattaacagaaaaagaaaaagc\ntgaactacaagcaaaacttgaagcagaagcaaaagcactcaaagaacaat\ntagcgAAACAAGCTGAAGAACTcGC"
isPcr_result_e = ""