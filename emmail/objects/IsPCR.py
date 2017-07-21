from os import path
from emmail.objects.Command import Command, FileNotInPathException

class IsPCR(Command):

    def __init__(self, assembly_filename, primer_filename, min_perfect, min_good,
                min_product_length, max_product_length, output_stream):
                
        Command.__init__(self, "isPcr")
        self.assembly_filename = Command.assert_filepath_and_return(assembly_filename)
        self.primer_filename = Command.assert_filepath_and_return(primer_filename)
        
        self.min_perfect = min_perfect
        self.min_good = min_good
        
        self.min_product_length = min_product_length
        self.max_product_length = max_product_length
        self.output_stream = output_stream
        
        self.command_string = self.build_isPcr_command()
    
    def __repr__(self):
        return self.command_string
    
    def build_isPcr_command(self):
            
        string = ("isPcr {db} {query} {output} "
                    "-minPerfect={} -minGood={} "
                    # "-minSize={} " Weirdly does not work.
                    "-maxSize={}")
        
        command = string.format(self.min_perfect,
                                self.min_good,
                                # self.min_product_length,
                                self.max_product_length,
                                db=self.assembly_filename, 
                                query=self.primer_filename, 
                                output=self.output_stream)
        
        return command
    
    def run_isPcr_pipeline(self):
        stdout = Command.run_command(self)
        return stdout