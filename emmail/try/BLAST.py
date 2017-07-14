from os import path
from Command import Command, FileNotInPathException
from Row import Row

class BLAST(Command):
    
    def __init__(self, db, query, dust,
                perc_identity, culling_limit,
                outfmt, out=None):
                
        Command.__init__(self, "blastn")
        
        self.db = self.assert_db_and_return(db)
        self.query = Command.assert_filepath_and_return(query)
        
        self.dust = dust
        self.perc_identity = perc_identity
        self.culling_limit = culling_limit
        
        self.outformat = outfmt
        self.output_stream = out
        
        self.command_string = self.build_blastn_command()
    
    def __repr__(self):
        return self.command_string
    
    def __str__(self):
        string = ("{0}\n"
                    "Query = {1}\n"
                    "DB = {2}\n"
                    "Dust filter = {3}\n"
                    "% Identity = {4}\nCulling limit = {5}\n"
                    "Outformat = {6}\nOutput to = {7}\n")
        
        string = string.format(self.version, self.query, self.db, self.dust, self.perc_identity, 
                                self.culling_limit, self.outformat, self.output_stream)
        
        return string
    
    def assert_db_and_return(self, file_path):
    
        if not (path.isfile(file_path+".nin") and path.isfile(file_path+".nhr") and path.isfile(file_path+".nsq")):
            raise FileNotInPathException("{} is not a BLAST database!".format(file_path))
            exit(1)
                
        return file_path
        
    def build_blastn_command(self):
        
        string = ("blastn -db {0} -query {1} -dust {2} -perc_identity {3}"
                    " -culling_limit {4} -outfmt {5}")
        
        command = string.format(self.db, self.query, self.dust,
                                self.perc_identity, self.culling_limit,
                                "\"{}\"".format(self.outformat))
        
        # string = ("echo -e \">name\nATGCCCGACAGATAGA\" | blastn -db {} -outfmt {}")
        
        return command
    
    def filter_blastn_rows(self, outputs):
        
        ok_results = [Row(output).filterMe() for output in outputs if Row(output).filterMe() is not None]
        
        return ok_results
    
    def alternate_filter_blastn_rows(self, outputs):
        
        def buildGenerator(outputs):
            for output in outputs:
                yield output
        
        ok_results = []
        
        for output in buildGenerator(outputs):    
            if Row(output).filterMe() is not None:
                ok_results.append(Row(output))
            
        return ok_results
    
    def write_where(self, filtered_outputs):
        string = ""
        
        for output in filtered_outputs:
            string += repr(output) + "\n"
        
        if self.output_stream == None or self.output_stream == "None":
            print(string[:-1])
        else:
            with open(self.output_stream, "w") as handle:
                handle.write(string[:-1])
            
        return string[:-1]
    
    def run_blastn_pipeline(self):
        
        stdout = Command.run_command(self)
            
        # Divide BLAST output to lines, and process whether to print stderr or not.
        outputs = stdout.split("\n")[:-1]
        
        filtered_outputs = self.filter_blastn_rows(outputs)
        
        return self.write_where(filtered_outputs)
        
    @staticmethod
    def generateBLASTobj(db, query, dust="no",
                        perc_identity=95, culling_limit=1,
                        outfmt="6 std slen"):
                        
        return BLAST(db, query, dust, perc_identity, culling_limit, outfmt)