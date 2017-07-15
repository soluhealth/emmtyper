from os import path
import shutil
import subprocess

from sys import exit
from abc import ABCMeta, abstractmethod

class FileNotInPathException(Exception):
    pass
	
class Command(object, metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, tool_name):
        
        self.tool_name = tool_name
        
        self.tool_path = self.get_tool_path()
        self.version = None
        self.command_string = ""
	
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
                
    def run_command(self, check_version=False):
        
        if check_version == True:
            command = "{} -version".format(self.tool_name)
        else:
            command = self.command_string
            
        process = subprocess.Popen(args=command, 
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        
        # Note: Move to Logging
        if stderr.decode("ascii") != "":
            print(stderr)
            exit(1)
            
        return stdout.decode("ascii")