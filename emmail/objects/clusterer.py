from collections import Counter

from numpy import array
from sklearn.preprocessing import normalize
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from emmail.objects.resultRow import ResultRow

class Clusterer:
    def __init__(self, blastOutputFile, output_stream, verbose=False, binwidth=500, linkage="ward"):
        self.isolate = blastOutputFile.split("/")[-1].split(".")[0]
        self.results, self.positions = self.extractFromFile(blastOutputFile)
        
        self.output_stream = output_stream
        self.verbose = verbose
        
        self.binwidth = binwidth
        self.linkage = linkage
        self.cluster_number = 1
        
    def __repr__(self):
        string = ("Clusterer for {} with binwidth {}bp, resulting in {} cluster(s)\n{} output to {}")
        
        return string.format(self.isolate, self.binwidth, self.cluster_number,
                            "Verbose" if self.verbose else "Short", self.output_stream)
    
    def extractFromFile(self, blastOutputFile):
        with open(blastOutputFile, "r") as handle:
            results = [ResultRow(line.strip()) for line in handle.readlines()]
            positions = array([(result.contig, result.queryStart, result.queryEnd) for result in results], dtype="float64")
        return results, positions
    
    def short_stringer(self):
        string = "{0}\t{1}\t{2}\t\t{3}".format(
                            self.isolate,
                            self.cluster_number,
                            ", ".join([str(answer) for answer in self.answer]), 
                            ", ".join([str(x) for x in self.possible_imposters 
                                       if x.score == 100]))
                            
        return string
    
    def verbose_stringer(self):
        string = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
                                        self.isolate, 
                                        len(self.results), 
                                        self.flag, 
                                        self.cluster_number, 
                                        ", ".join([str(answer) for answer in self.answer]),
                                        ", ".join(["{}:{}".format(answer.contig, answer.queryStart) for answer in self.answer]),
                                        ", ".join([str(x) for x in self.possible_imposters
                                                    if x.score == 100]),
                                        ", ".join(["{}:{}".format(x.contig, x.queryStart) for x in self.possible_imposters
                                                    if x.score == 100]))
        
        return string
    
    def visual_c(self, threshold=100):
        ### EXPERIMENTAL ###
        # Visual map of emm hits within WGS
        flag = 0
        answer = [answer for answer in self.results 
                        if answer.score == 100 and answer.type not in EmmImposters]
        
        possible_imposters = [x for x in self.results 
                                    if x.score >= threshold and x != answer[0]]
        
        string = "({})".format(answer[0])
        
        for imposter in possible_imposters:
            distance = abs(imposter.queryStart - answer[0].queryStart) // 500
            if imposter.queryStart < answer[0].queryStart:
                string = "{} {} ".format(imposter, "-" * distance) + string
            elif imposter.queryStart > answer[0].queryStart:
                string = string + " {} {}".format("-" * distance, imposter)
                
        return "{}\t{}".format(self.isolate, string)
    
    def get_best_scoring(self, results):
        try:
            maxScore = max([result.score for result in results])
            maxResult = [result for result in results if result.score == maxScore]
            
            return maxResult
            
        except ValueError:
            # When there is no result to iterate over, return null ResultRow
            return [ResultRow("0\tEMM0.0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0")]
            
    def get_cluster_with_max_vote(self, clusters_counter):
        count = clusters_counter.items()
        maximum_occurence = max([occ for clust, occ in count])
        
        return [clust for clust, occ in count if occ == maximum_occurence]
            
    def clust(self):
        best_score = self.get_best_scoring(self.results)
        
        if len(best_score) == 1:
            self.flag = 1
            self.answer = [best_score[0]]
            self.possible_imposters = [res for res in self.results
                                        if res not in self.answer and res.score == 100]
        
        else:
            self.flag = 2
            Z = linkage(self.positions, self.linkage)
            
            clusters = fcluster(Z, self.binwidth, criterion='distance')
            
            self.cluster_number = max(clusters)
            
            maxCluster = [result for key, result in enumerate(self.results) if clusters[key] in self.get_cluster_with_max_vote(Counter(clusters))]
            otherClusters = [result for key, result in enumerate(self.results) if clusters[key] not in self.get_cluster_with_max_vote(Counter(clusters))]

            self.answer = [result for result in self.get_best_scoring(maxCluster)]
            self.possible_imposters = [result for result in otherClusters]
    
    def main(self):
        self.clust()
        
        final_result =  self.verbose_stringer() if self.verbose else self.short_stringer()
        # final_result = self.quicker(threshold=100)
        
        if self.output_stream in [None, "None", "stdout"]:
            print(final_result)
        else:
            with open(self.output_stream, "w") as handle:
                handle.write(final_result)
                
        return final_result