from os import path, environ
import logging
import subprocess

from emmail.objects.Command import Command, FileNotInPathException
from emmail.objects.Row import Row

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

class BLAST(Command):
    
    def __init__(self, db, query, dust,
                perc_identity, culling_limit,
                output_stream, header,
                mismatch, align_diff, gap):
                
        Command.__init__(self, "blastn")
        
        self.version = self.get_version()
        
        self.db = self.assert_db_and_return(db)
        self.query = Command.assert_filepath_and_return(query)
        
        self.dust = dust
        self.perc_identity = perc_identity
        self.culling_limit = culling_limit
        
        self.outformat = "6 std slen"
        self.output_stream = output_stream
        
        self.want_header = header
        
        # Threshold for row filtering
        
        self.mismatch = mismatch
        self.align_diff = align_diff
        self.gap = gap
        
        self.command_string = self.build_blastn_command()
    
    def __repr__(self):
        return self.command_string
    
    def __str__(self):
        string = ("{0}\n"
                    "Query = {1}\n"
                    "DB = {2}\n"
                    "Dust filter = {3}\n"
                    "% Identity = {4}\n"
                    "Culling limit = {5}\n"
                    "Outformat = {6}\n"
                    "Output to = {7}\n"
                    "Mismatch filter = {8}\n"
                    "Align difference filter = {9}\n"
                    "Gap filter = {10}")
        
        string = string.format(self.version, self.query, self.db, self.dust, self.perc_identity, 
                                self.culling_limit, self.outformat, self.output_stream,
                                self.mismatch, self.align_diff, self.gap)
        
        return string
    
    def get_version(self):
        process = subprocess.Popen(args="{} -version".format(self.tool_name), 
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        
        return stdout.decode("ascii")
    
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

        return command
    
    def filter_blastn_rows(self, outputs):
        
        ok_results = [Row(output).filterMe(self.mismatch, self.align_diff, self.gap) 
                        for output in outputs 
                        if Row(output).filterMe(self.mismatch, self.align_diff, self.gap) 
                        is not None]
        
        return ok_results
    
    def row_to_output(self, filtered_outputs):
        string = ""
        
        # I want to run this without repr
        for output in filtered_outputs:
            string += repr(output) + "\n"
        
        if string:
            if self.want_header:
                string = Row.buildHeader() + string
                
            if self.output_stream in [None, "None", "stdout"]:
                print(string[:-1])
            else:
                with open(self.output_stream, "w") as handle:
                    handle.write(string[:-1])
                
        else:
            logger.info("There is no output for {}".format(self.query))
        
        return string[:-1]
        
    def run_blastn_pipeline(self):
        logger.info("Running on {}".format(self.query))
        
        outputs = Command.run(self).split("\n")[:-1]
        
        filtered_outputs = self.filter_blastn_rows(outputs)
        
        return self.row_to_output(filtered_outputs)