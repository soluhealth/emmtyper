'''
Define the isPCR class
'''
from os import path, environ
import logging
import subprocess
import shlex
import pathlib

from emmtyper.objects.command import Command, FileNotInPathException

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class IsPCR(Command):
    '''
    Run isPCR. Inherits from Command
    '''
    def __init__(
        self,
        assembly_filename,
        primer_filename,
        min_perfect,
        min_good,
        tile_size,
        step_size,
        max_product_length,
        output_stream,
        tool_path=None,
    ):

        Command.__init__(self, "isPcr", tool_path=tool_path)

        self.assembly_filename = shlex.quote(
            Command.assert_filepath_and_return(assembly_filename)
        )
        self.primer_filename = shlex.quote(
            Command.assert_filepath_and_return(primer_filename)
        )

        self.min_perfect = min_perfect
        self.min_good = min_good

        self.tile_size = tile_size
        self.step_size = step_size

        self.max_product_length = max_product_length
        self.output_stream = output_stream

        self.command_string = self.build_isPCR_command()

    def __repr__(self):
        return self.command_string

    def build_isPCR_command(self):

        string = (
            "{tool_path} {db} {query} {output} "
            "-minPerfect={min_perfect} -minGood={min_good}"
            #" -tileSize={tile_size} -stepSize={step_size}"
            " -tileSize={tile_size}"
            " -stepSize={step_size}"
            " -maxSize={max_size}"
        )

        command = string.format(
            min_perfect=self.min_perfect,
            min_good=self.min_good,
            tile_size=self.tile_size,
            step_size = self.step_size,
            max_size=self.max_product_length,
            db=self.assembly_filename,
            query=self.primer_filename,
            output=self.output_stream,
            tool_path=self.tool_path,
        )
        logger.info(command)

        return command

    def run_isPCR(self):
        # logger.info("Running on {}".format(self.assembly_filename))

        output = Command.run(self)

        if not output:
            logger.info("There is no output for {}".format(self.assembly_filename))

        #remove the primer in contigs headers
        new_out = []
        for line in output.split("\n"):
            if len(line) > 0:
                if line[0] == ">":
                    new_line = " ".join(line.split()[:-2])
                    new_out.append(new_line)
                else:
                    new_out.append(line)
            else:
                new_out.append(line)
        return "\n".join(new_out)
        #return output[:-1]
