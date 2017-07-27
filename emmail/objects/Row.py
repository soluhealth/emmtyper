class wrongLengthException(Exception):
	pass

class Row:
    variableList = ['Query', 'BlastHit', 'Identity', 'AlignmentLength', 'Mismatch',
                    'GapOpen', 'QueryStart', 'QueryEnd', 'HitStart', 'HitEnd',
                    'E-Value', 'BitScore', 'SubjectLength']

    def __init__(self, string):
        self.fullRow = string
    
        rowSplit = string.split("\t")
        
        if len(self.variableList) != len(rowSplit):
            raise wrongLengthException("Wrong row length!")
        
        rowSplit[3:10] = map(int, rowSplit[3:10])
        rowSplit[12:14] = map(int, rowSplit[12:14])
        
        (query, blastHit, identity, alignmentLength, mismatch, 
        gapOpen, queryStart, queryEnd, hitStart, hitEnd, 
        eValue, bitScore, subjectLength) = rowSplit

        self.Query = query
        self.BlastHit = blastHit
        
        self.Identity = float(identity)
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
            
    def __repr__(self):
        return self.fullRow
    
    def __str__(self):
        string = "Contig {0} has hit {1} with {2} identity and {3}bps alignment"
        
        return (string.format(self.Query, self.BlastHit, self.Identity, self.AlignmentLength))
    
    @staticmethod
    def buildHeader():
        header = ""
        
        for variable in Row.variableList:
            header += variable + "\t"
            
        return header[:-1] + "\n"
    
    def filterMe(self, mismatch, align_diff, gap):
        if (self.mismatch_k(mismatch) and self.alignment_to_subject_length_k(align_diff) and self.gap_k(gap)):
            return self
    
    ### Filter functions.

    def alignment_to_subject_length_k(self, k = 0):
        # Check whether alignment length is within minimum k threshold to subject length.

        return (self.SubjectLength - self.AlignmentLength) <= k

    def mismatch_k(self, k = 0):
        # Accounts possibility of k mismatch(es) as okay for classification.

        return self.Mismatch <= k

    def gap_k(self, k = 0):
        # Check whether there are k (or less) gaps in Row instance.

        return self.GapOpen <= k

    ### Prototype filter functions. Currently not used.

    def hit_start_end_k(self, k = 0):
        # Reduces need for alignment length to be same as subject length by k value.
        # Requires other functions to work well, such as mismatch functions.

        start = 1 + k
        end = self.SubjectLength - k

        start_bool = self.HitStart <= start or self.HitStart >= end
        end_bool = self.HitEnd <= start or self.HitEnd >= end

        return start_bool and end_bool

    def bit_score_346(self, bit = 346):
        # Check whether bit score is full.

        return self.BitScore == bit