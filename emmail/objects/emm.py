import os

def find(filename):
    for root, dirs, files in os.walk(os.path.dirname(__file__), topdown=False):
        for name in files:
            if name == filename:
                return os.path.join(root, name)

cluster_translations = dict()

with open(find("emm_clusters.csv")) as handle:
    for line in handle.readlines():
        emm, cluster = line.split(",")
        cluster_translations[emm] = cluster.strip()

# Add nonexistent EMM0 as null result
cluster_translations["0"] = "-"
        
class EMM:
    def __init__(self, string):
        self.number = "".join([char for char in string if char.isdigit()])
        self.code = "".join([char for char in string if not char.isdigit()])
        self.emm_cluster = self.translate_to_cluster()
    
    def translate_to_cluster(self):
        if self.code == "EMM":
            return cluster_translations[self.number]
        
        return cluster_translations["0"]
    
    def __str__(self):
        return "{} is in Cluster {}".format(self.blastHit, self.emm_cluster)