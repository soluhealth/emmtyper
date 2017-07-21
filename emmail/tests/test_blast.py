# from emmail.objects.Command import Command
from emmail.objects.BLAST import BLAST

db = "/home/andret1/projects/blastDB/8Jun17.fasta"
test_sequence_path = "contig.fasta"

b = BLAST(db, test_sequence_path, dust="no",
          perc_identity=95, culling_limit=1,
          outfmt="6 std slen")

print(repr(b))
print(b.version)
b.run_blastn_pipeline()