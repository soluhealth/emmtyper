import numpy as np
from os.path import isfile
from emmail.objects.resultRow import ResultRow, EmmImposters
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

nullResult = ResultRow("0\tEMM0.0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0") 

class Clusterer:
    def __init__(self, blastOutputFile, output_stream, verbose=False, distance=500, linkage="ward"):
        self.isolate = blastOutputFile
        self.results = self.extractFromFile(blastOutputFile)
        
        self.output_stream = output_stream
        self.verbose = verbose
        
        self.clust_distance = distance
        self.linkage = linkage
        
        self.cluster_number = 0
        self.ascii_vis = self.isolate
    
    def __repr__(self):
        string = ("Clusterer for {} with binwidth {}bp, resulting in {} cluster(s)\n{} output to {}")
        
        return string.format(self.isolate, self.clust_distance, self.cluster_number,
                            "Verbose" if self.verbose else "Short", self.output_stream)
    
    def extractFromFile(self, blastOutputFile):
        with open(blastOutputFile, "r") as handle:
            results = [ResultRow(line.strip()) for line in handle.readlines()]
            
        return results
# Use the logic mentioned by Anders, need something with the visualization as well

    def string_a_magic(self, result, score=92):
        
        if type(result) is ResultRow and result.score >= score:
            return [result]
        elif type(result) is list:
            tmp = []
            for res in result:
                if res.score >= score:
                    tmp.append(res)
            return tmp
        return [nullResult]
        
    def short_stringer(self):
        header = "Isolate\tNumberOfClusters\tAnswers\tSuspectImposters\n"
        string = "{0}\t{1}\t{2}\t{3}".format(
                            self.isolate,
                            self.cluster_number,
                            ";".join([str(answer) for answer in self.string_a_magic(self.answers)]), 
                            ";".join([str(x) for x in self.possible_imposters]))

        string = header+string
        return string
    
    def verbose_stringer(self):
        header = "Isolate\tNumberOfHits\tNumberOfClusters\tAnswers\tAnswerPositions\tSuspectImposters\tSuspectPositions\n"
        string = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(
                                        self.isolate, 
                                        len(self.results), 
                                        self.cluster_number, 
                                        ";".join([str(answer) for answer in self.answers]),
                                        ";".join(["{}:{}".format(answer.contig, answer.queryStart) for answer in self.answers]),
                                        ";".join([str(x) for x in self.possible_imposters
                                                    if x.score >= 92]),
                                        ";".join(["{}:{}".format(x.contig, x.queryStart) for x in self.possible_imposters
                                                    if x.score >= 92]))
        
        string = header+string
        return string
    
    def cluster(self, results):
        if len(results) == 1:
            return [1]
        
        elif len(results) >= 2:
            positions = [result.positions for result in results]
            Z = linkage(positions, self.linkage)
            clusters = fcluster(Z, self.clust_distance, criterion="distance")
            
            return clusters
        
        else:
            raise Exception("Cannot run with {} results.".format(len(positions)))
            
    def get_best_scoring(self, results):
        try:
            maxScore = max([result.score for result in results])
            maxResult = [result for result in results if result.score == maxScore]
            
            if len(maxResult) == 1:
                return maxResult[0]
            else:
                if (set([result.score for result in maxResult])) == set([100]):
                    # To check possibility of multiple 100 scoring results
                    # THIS IS OUR PROBLEM WITH 39.4 and 39.1
                    return maxResult
                else:
                    # If scores are not 100, take random result from the array
                    pos = np.random.randint(len(maxResult), size=1)[0]
                    return maxResult[pos]
            
        except ValueError:
            # When there is no result, return a null ResultRow object.
            return nullResult      
    
    def best_in_cluster_in_contig(self, contig):
        # Extract results that fall within contig and cluster them together
        within_contig = np.array([result for result in self.results if result.positions[0] == contig])
        contig_cluster = self.cluster(within_contig)
        
        # Look for best-scoring within each cluster and return as a list of best results in contig.
        if len(within_contig) == 1:
            return [(1, within_contig[0])]
        
        else:
            answer = []

            for cluster in set(contig_cluster):           
                within_cluster = within_contig[contig_cluster == cluster]
                answer.append((len(within_cluster), self.get_best_scoring(within_cluster)))

        return answer
    
    def classify_expected_answer(self, max_iteration=10):
        try:
            votes = np.array([[item[0], item[1]] for item in self.best_in_clusters])
            answers_w_max_vote = votes[votes[:, 0] == max(votes[:, 0]), :]

            try:
                answers = [answer for answer in answers_w_max_vote 
                           if answer[1].type not in EmmImposters and answer[1].score == 100]

                if answers == []:
                    for i in range(max_iteration): # Look for result with next maximum votes up until how many times.
                        new_votes = votes[[~np.isin(votes[:,1], answers_w_max_vote[:,1])]]

                        try:
                            answers_w_max_vote = new_votes[new_votes[:, 0] == max(new_votes[:, 0]), :]
                            answers = [answer for answer in answers_w_max_vote if answer[1].type not in EmmImposters]
                        except ValueError: # If list is empty, max() will return ValueError
                            answers = [answer for answer in answers_w_max_vote if answer[1].score == 100]

                if answers == []: # If still empty, ignore EmmImposters filter
                    answers = [answer for answer in answers_w_max_vote]
                
            except AttributeError: # If there are multiple answers_w_max_vote, this will be returned
                #print("vote", answers_w_max_vote)
                answers = answers_w_max_vote[np.random.randint(answers_w_max_vote.shape[0], size=1)[0], :].reshape(1,2)[:,1]
                # print("answers", answers)
            
            # self.Answers does not accomodate list within list.
            # So 39.1 always taken. Obviously we need another way to discern list of list and list of ResRow
            self.answers = list(answer[1] for answer in answers)
            # print(self.answers)
            self.possible_imposters = list(votes[~np.isin(votes[:,1], answers), 1])
            
        except IndexError: # When there is no result to show
            self.answers = [nullResult]
            self.possible_imposters = [nullResult]
            print("aw")
            
    def visualize_contig(self, contig):
        ### EXPERIMENTAL ###
        # Visual map of emm hits within WGS
        
        def determine_position(result):
            if type(result) is ResultRow:
                return result.queryStart
            elif type(result) is list:
                return sum([p.queryStart for p in result])/len(result)
            else:
                raise Exception("Something is wrong in visContig")
                
        contig = [result[1] for result in contig]
        string = ""
        
        for j, pos in enumerate(contig): # List of results with best score in cluster
            hit = str(pos)
            position = determine_position(pos)
            
            if j == 0:
                string += hit
            else:
                distance = int((position - prevPos) // self.clust_distance)
                if distance < 0:
                    string = "{}{}{}".format(hit, "-" * abs(distance), string)
                else:
                    string = "{}{}{}".format(string, "-" * abs(distance), hit)
            
            prevPos = position
            
        return string    
    
    def main(self):
        if len(self.results) > 0:
            self.best_in_clusters = []

            for i in set([result.positions[0] for result in self.results]): # For every contig
                contig_best = self.best_in_cluster_in_contig(i)
                self.best_in_clusters.extend(contig_best)
                
                self.cluster_number += len(contig_best)
                self.ascii_vis += "\t" + self.visualize_contig(contig_best)
            
            # Now get final answer
            self.classify_expected_answer()

            final_result =  self.verbose_stringer() if self.verbose else self.short_stringer()

            if self.output_stream in [None, "None", "stdout"]:
                print(final_result)
            else:
                # print(final_result)                
                with open(self.output_stream, "a") as handle:
                    handle.write(final_result+"\n")
            
            return final_result
        
        else:
            return # DO SOMETHING HERE