from os import path, environ
import shutil
import subprocess
import logging

from sys import exit
from abc import ABCMeta, abstractmethod, abstractproperty

logging.basicConfig(level=environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger()

class FileNotInPathException(Exception):
    pass
	
class Command(object, metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, tool_name):
        
        self.tool_name = tool_name
        
        self.tool_path = self.get_tool_path()
        self.version = None
        self.command_string = None
        self.output_stream = None
    
    def get_tool_path(self):
        """Check whether tool exists. If True, return path to the tool."""
        tool_path = shutil.which(self.tool_name)
		
        if tool_path == None:
            raise FileNotInPathException("{} does not exist in $PATH!".format(self.tool_name))
            exit(1)
        
        return tool_path
    
    @staticmethod
    def assert_filepath_and_return(file_path):
        
        if not path.isfile(file_path):
            raise FileNotInPathException("{} is not a file!".format(file_path))
            exit(1)
            
        return file_path
    
    def run(self):
        process = subprocess.Popen(args=self.command_string, 
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()

        if stderr.decode("ascii"):
            logger.warning("{}: {}".format(self.tool_name, stderr.decode("ascii")[:-1]))
        
        return stdout.decode("ascii")