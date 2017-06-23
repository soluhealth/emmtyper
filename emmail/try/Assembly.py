from Bio import SeqIO
import os.path

class Assembly:
	def __init__(self, filename):
		assert self.path_exists(filename), "File does not exist!"
		
		self.Id = filename[:filename.index(".")]
		
		self.Assembly = []
		self.Assembly = self.iterateAndAppend_toAssembly(filename)
		
		self.Type = None
		
	def __repr__(self):
		string = "Assembly {} of {} contigs totaling {}bps"
		return string.format(self.Id, self.get_contig_number(), self.get_total_size())
	
	def __len__(self):
		return self.get_total_size()
		
	def get_contig_number(self):
		return len(self.Assembly)
	
	def get_total_size(self):
		lengths = map(len, self.Assembly)
		return sum(lengths)
	
	def iterateAndAppend_toAssembly(self, filename):
		with open(filename, "rU") as handle:
			for record in SeqIO.parse(handle, "fasta"):
				self.Assembly.append(str(record.seq))
		
		return self.Assembly
		
	def set_type(self, scheme, type):
		self.Type = (scheme, type)
	
	def path_exists(self, filename):
		return os.path.isfile(filename)
		
	