class wrongLengthException(Exception):
	pass

class Row:
	variableList = ['Query', 'Blast Hit', 'Identity', 'Alignment Length', 'Mismatch',
					'Gap Open', 'Query Start', 'Query End', 'Hit Start', 'Hit End',
					'E-Value', 'Bit Score', 'Subject Length']
	
	def __init__(self, string):
		
		if len(self.variableList) != len(string.split("\t")):
			raise wrongLengthException("Wrong row length!")
		
		stringSplit = string.split("\t")
		
		stringSplit[2:10] = [int(x) for x in stringSplit[2:10]]
		stringSplit[11:] = [int(x) for x in stringSplit[11:]]
		
		(query, blastHit, identity, alignmentLength, mismatch, 
		gapOpen, queryStart, queryEnd, hitStart, hitEnd, 
		eValue, bitScore, subjectLength) = stringSplit

		self.Query = query
		self.BlastHit = blastHit
		self.Identity = identity
		self.AlignmentLength = alignmentLength
		self.Mismatch = mismatch
		self.GapOpen = gapOpen
		self.QueryStart = queryStart
		self.QueryEnd = queryEnd
		self.HitStart = hitStart
		self.HitEnd = hitEnd
		self.EValue = eValue
		self.BitScore = bitScore
		self.SubjectLength = subjectLength
		
	def get_query(self):
		return self.Query
		
	def get_blastHit(self):
		return self.BlastHit
	
	def get_mismatch(self):
		return self.Mismatch
	
	def get_subjectLength(self):
		return self.SubjectLength