from collections import Counter

from numpy import array
from sklearn.cluster import KMeans
from sys import argv, stdin

from emmail.objects.resultRow import ResultRow

class Clusterer:
    def __init__(self, blastOutputFile, output_stream, verbose=False, binwidth=800):
        self.isolate = blastOutputFile.split("/")[-1].split(".")[0]
        self.results, self.positions, self.starts = self.extractFromFile(blastOutputFile)
        
        self.output_stream = output_stream
        self.verbose = verbose
        self.binwidth = binwidth
        
        self.cluster_number = self.get_cluster_number()
        
        self.flag = 0
        self.answer = ""
        self.possible_imposters = []
        self.others = ""
        
    def extractFromFile(self, blastOutputFile):
        with open(blastOutputFile, "r") as handle:
            results = [ResultRow(line.strip()) for line in handle.readlines()]
            positions = [(result.queryStart, result.queryEnd) for result in results]
            starts = [result.queryStart for result in results]
        return results, positions, starts

    def get_best_scoring(self, results):
        maxScore = max([result.score for result in results])
        maxResult = [result for result in results if result.score == maxScore]
        
        return maxResult
    
    def get_cluster_number(self):
        bins = range(min(self.starts), max(self.starts) + self.binwidth, self.binwidth)
        binnings = [0] * (len(bins) - 1)
        
        for idx in range(len(bins) - 1):
            for start in self.starts:
                if start >= bins[idx] and start <= bins[idx+1]:
                    binnings[idx] += 1
        
        cluster_w_hits = sum([1 for bin in binnings if bin > 0])
        
        return cluster_w_hits if cluster_w_hits > 0 else 1
            
    def clust(self):
        best_score = self.get_best_scoring(self.results)
        
        if len(best_score) == 1:
            self.flag = 1
            self.answer = [best_score[0]]
            self.possible_imposters = [res.blastHit for res in best_score 
                                        if res.score == 100 and res.type != self.answer[0].type]
            
        else:
            self.flag = 2
            
            kmeans = KMeans(n_clusters=self.cluster_number).fit(self.positions)
           
            maxCluster = [result for key, result in enumerate(self.results) if kmeans.labels_[key] == Counter(kmeans.labels_).most_common()[0][0]]
            otherClusters = [result for key, result in enumerate(self.results) if kmeans.labels_[key] != Counter(kmeans.labels_).most_common()[0][0] and result.score == 100]
            
            self.answer = [result for result in self.get_best_scoring(maxCluster)]
            self.possible_imposters = [result for result in otherClusters]
                
    def update_additional_information(self):
        EmmImposters = ["EMM51", "EMM138", "EMM149", "EMM156",
                    "EMM159", "EMM164", "EMM170", "EMM174", 
                    "EMM202", "EMM205", "EMM236", "EMM240"]        
    
        for result in self.answer:
            if result.type in EmmImposters:
                self.others = "Suspect"
            if result.score != 100:
                self.others = "Not100"
    
    def short_stringer(self):
        string = "{0}\t{1}\t{2}\t{3}".format(
                            self.isolate,
                            ", ".join([str(answer) for answer in self.answer]), 
                            ", ".join([str(answer) for answer in self.possible_imposters]) if len(self.possible_imposters) > 1 else "",
                            self.others)
                            
        return string
    
    def verbose_stringer(self):
        string = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(
                                        self.isolate, 
                                        len(self.results), 
                                        self.flag, 
                                        ", ".join([x.blastHit for x in self.answer]),
                                        [x.score for x in self.answer],
                                        [x.queryStart for x in self.answer],
                                        self.cluster_number, 
                                        self.possible_imposters,
                                        self.others)
        return string
    
    def main(self):
        self.clust()
        self.update_additional_information()
        
        final_result =  self.verbose_stringer() if self.verbose else self.short_stringer()
        
        if self.output_stream in [None, "None", "stdout"]:
            print(final_result)
        else:
            with open(self.output_stream, "w") as handle:
                handle.write(final_result)
                
        return final_result