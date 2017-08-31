from emmail.objects.resultRow import ResultRow, EmmImposters

from collections import Counter

from numpy import array
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import normalize, scale
from sklearn.metrics import silhouette_score, calinski_harabaz_score

class Clusterer:
    def __init__(self, blastOutputFile, output_stream, verbose=False, binwidth=800):
        self.isolate = blastOutputFile.split("/")[-1].split(".")[0]
        self.results, self.positions = self.extractFromFile(blastOutputFile)
        
        self.output_stream = output_stream
        self.verbose = verbose
        self.binwidth = binwidth
        
        self.cluster_number = 1
        
        self.flag = 0
        self.answer = ""
        self.possible_imposters = []
        
    def extractFromFile(self, blastOutputFile):
        with open(blastOutputFile, "r") as handle:
            results = [ResultRow(line.strip()) for line in handle.readlines()]
            positions = array([(result.contig, result.queryStart, result.queryEnd) for result in results], dtype="float64")
        return results, positions
    
    def short_stringer(self):
        string = "{0}\t{1}\t\t{2}".format(
                            self.isolate,
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

    def get_best_scoring(self, results):
        maxScore = max([result.score for result in results])
        maxResult = [result for result in results if result.score == maxScore]
        
        return maxResult
    
    def get_cluster_with_max_vote(self, clusters_counter):
        count = clusters_counter.items()
        maximum_occurence = max([occ for clust, occ in count])
        
        return [clust for clust, occ in count if occ == maximum_occurence]
    
    def get_cluster_number_elbow(self):
        # USING SILHOUETTE
        
        try:
            tmp_s = float("inf")
            
            for cluster in range(2, self.positions.shape[0] + 1):
                model = KMeans(n_clusters=cluster).fit(normalize(self.positions, axis = 0))
                s_score = silhouette_score(self.positions, model.labels_)
                # print("silhouette score is {} for {} cl".format(s_score, cluster))
                
                # If residuals do not decrease, return the previous cluster
                if tmp_s == s_score:
                    return cluster-1
                
                tmp_s = s_score
            
            return 1    
            #print("flag 3 = {}".format(cluster_number))
            
        except ValueError:
            return self.positions.shape[0]
    
    def get_cluster_number_ch(self):
        # USING CALINSKI HARABAZ
        max_ch_score = 1
        cluster_number = 1
        
        try:
            for cluster in range(2, self.positions.shape[0] + 1):
                model = KMeans(n_clusters=cluster).fit(normalize(self.positions, axis = 0))
                ch_score = calinski_harabaz_score(self.positions, model.labels_)
                # print("ch score is {} for {} cl".format(ch_score, cluster))
                
                if ch_score <= max_ch_score:
                    return cluster
                
                max_ch_score = ch_score
            
            return 1
            #print("flag 3 = {}".format(cluster_number))
        
        except ValueError:
            return self.positions.shape[0]
    
    def quicker_c(self, threshold=100):
        ### EXPERIMENTAL ###
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
    
    def clust(self):
        best_score = self.get_best_scoring(self.results)
        
        if len(best_score) == 1:
            self.flag = 1
            # print("no clustering done")
            self.answer = [best_score[0]]
            self.possible_imposters = [res for res in self.results
                                        if res not in self.answer and res.score == 100]
        
        else:
            self.flag = 2
            self.cluster_number = self.get_cluster_number_elbow()
            # print("clustering for {}".format(self.cluster_number))
            model = AgglomerativeClustering(n_clusters=self.cluster_number).fit(normalize(self.positions, axis = 0))
            
            # [print(self.positions[i].astype("int32"), self.results[i], model.labels_[i]) for i in range(len(self.positions))]
                
            maxCluster = [result for key, result in enumerate(self.results) if model.labels_[key] in self.get_cluster_with_max_vote(Counter(model.labels_))]
            otherClusters = [result for key, result in enumerate(self.results) if model.labels_[key] not in self.get_cluster_with_max_vote(Counter(model.labels_))]

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