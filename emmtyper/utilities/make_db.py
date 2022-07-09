"""
Update and make a BLAST DB from a new DB FASTA file
"""

import subprocess
import ftplib
import logging
import datetime
from dateutil import parser
import json
import pathlib
import os
import tempfile
import shutil
from typing import List, Dict

import click


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging

def decode_history(dct: dict) -> dict:
    """
    Decode the history dictionary from JSON to a Python dictionary.
    """
    dct['updated_on'] = datetime.datetime.strptime(dct["updated_on"], "%Y-%m-%d") if dct["updated_on"] else ""
    dct['uploaded_to_server_on'] = datetime.datetime.strptime(dct["uploaded_to_server_on"], "%Y-%m-%d") if dct["uploaded_to_server_on"] else ""
    return dct

def encode_history(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d")
    return obj

class DBMetadata:
    """
    Store and update the DB Metadata
    """

    def __init__(self, metadata_db):
        self.path = pathlib.Path(metadata_db)
        self.db_folder = self.path.parent
        self.history = []
        self.update_dupes = []
        self.update_total_seqs = 0
        if self.path.exists():
            with open(self.path) as history:
                self.history = json.load(history, object_hook=decode_history)
                self.history = sorted(self.history, key=lambda k: k["updated_on"])
                self.metad = self.history[-1]
        else:
            self.metad = {
                    "updated_on": f"{datetime.datetime.today():%Y-%m-%d}",
                    "host": "ftp.cdc.gov",
                    "filename": "/pub/infectious_diseases/biotech/tsemm/trimmed.tfa",
                    "uploaded_to_server_on": "",
            }

    def needs_updating(self, new_date):
        LOGGER.debug(
            f"Is {new_date:%Y-%m-%d} later than {self.uploaded_to_server_on:%Y-%m-%d}?: {new_date.date() > self.uploaded_to_server_on.date()}"
        )
        return new_date.date() > self.uploaded_to_server_on.date()

    def update_info(self, key, value):
        try:
            self.metad[key] = value
        except KeyError as error:
            print(error)
            pass

    def update_metadata_file(self):
        self.history.append(self.metad)
        with open(self.path, "w") as metajson:
            json.dump(self.history, metajson, default=encode_history, indent=4)

    def make_db(self, fasta_file):
        '''
        Main function to generate a BLAST DB
        '''
        title = f'"EMM DB created on {datetime.date.today():%Y-%m-%d}"'
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            LOGGER.info("Making BLAST DB...")
            LOGGER.debug(f"Working in temp folder {tmpdir}...")
            LOGGER.debug(f"Original FASTA file: {str(fasta_file.absolute())}")
            fasta_name = fasta_file.name
            shutil.copy(str(fasta_file.absolute()), fasta_name)
            clean_db = f'seqkit rmdup -s -D dupes.txt {fasta_name} > {fasta_name}.clean'
            LOGGER.debug(f"Checking for duplicates in the FASTA file: {clean_db}")
            subprocess.run(clean_db, shell=True, check=True)
            with open("dupes.txt", "r") as dupes:
                dupes = dupes.readlines()
            if len(dupes) > 0:
                # create a backup copy of the original FASTA
                shutil.copy(fasta_name, fasta_name + ".orig")
                LOGGER.warning(f"Found {len(dupes)} duplicate sequences in {fasta_name}")
                LOGGER.warning("Cleaning up duplicates...")
                dupes = [d.strip().split("\t")[1].replace(", ", ":") for d in dupes]
                dupes = [f"{d.split(':')[0]}\t{d}" for d in dupes]
                self.update_dupes = dupes
                with open("replacements.txt", "w") as replacements:
                    replacements.write("\n".join(dupes))
                relabel_db = f"seqkit replace -r '{{kv}}${{2}}' -k replacements.txt -p '(\w+\.\d+)( .*)$' -K {fasta_name}.clean > {fasta_name}"
                subprocess.run(relabel_db, shell=True, check=True)
            self.update_total_seqs = int(subprocess.run(f"grep '>' {fasta_name} | wc -l", shell=True, capture_output=True, encoding='utf-8').stdout.strip())
            cmd = f'makeblastdb -in "{fasta_name}" -dbtype nucl -title {title}'
            LOGGER.info(f"Running command: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
                dest = str(fasta_file.parent)
                for fn in os.listdir():
                    if fasta_name in fn:
                        LOGGER.debug(f"Copying {fn} to {dest}")
                        shutil.copy(fn, dest)
            except subprocess.CalledProcessError as error:
                LOGGER.exception(error)
                raise
            self.update_info("total_seqs", self.update_total_seqs)
            self.update_info("total_duplicate_seqs", len(self.update_dupes))
            self.update_info("duplicated_seqs", self.update_dupes)


def download_cdc_db(
    db_folder, passwd, user="anonymous", db_metadata="db_metadata.json"
):
    '''
    Download the CDC DB.
    '''
    db_path = pathlib.Path(db_folder)
    db_path.mkdir(parents=True, exist_ok=True)
    db_metadata = db_path / db_metadata
    db_fasta = db_path / "emm.fna"
    db = DBMetadata(db_metadata)
    filename = db.metad["filename"]
    host = db.metad["host"]
    con = ftplib.FTP(host=host, user=user, passwd=passwd)
    updated_on = f"{datetime.datetime.today():%Y-%m-%d}"
    modified_time = parser.parse(con.sendcmd("MDTM " + filename)[4:])
    if db.needs_updating(modified_time):
        with open(db_fasta, "wb") as emm_fa:
            con.retrbinary(f"RETR {filename}", emm_fa.write)
        try:
            if db_fasta.exists():
                make_db(db_fasta, updated_on)
                db.update_info("updated_on", updated_on)
                db.update_info("uploaded_to_server_on", f"{modified_time:%Y-%m-%d}")
                db.update_metadata_file()
            else:
                raise FileNotFoundError
        except FileNotFoundError as error:
            LOGGER.exception(error)
    else:
        LOGGER.info("EMM DB is up-to-date.")


def get_db_folder():
    """
    Check if EMM_DB is in the os.environ, else return the location of the DB in the package.

    If not writable, make another suggestion in the users /home folder
    """
    db_folder = os.environ.get(
        "EMM_DB", pathlib.Path(__file__).absolute().parent.parent / "db"
    )
    try:
        test_file = db_folder / "test.txt"
        with open(test_file, "w") as testf:
            testf.write("testing")
        test_file.unlink()
    except PermissionError:
        try:
            db_folder = pathlib.Path.home() / "emm_db"
            db_folder.mkdir()
        except FileExistsError as error:
            pass
        except Exception as error:
            LOGGER.exception(error)
    return db_folder


@click.command()
@click.argument("email")
@click.option(
    "--db_folder",
    "-d",
    help="Where to update the DB",
    default=get_db_folder(),
    show_default=True,
)
def emmtyper_db(email, db_folder):
    """\
    EMAIL is needed to connect to CDC FTP server.

    By default, db_folder will be taken from EMM_DB environmental folder.
    If can't find the folder, will default to where emmtyper
    is installed. If it cannot write to the installation folder,
    it will make a suggestion in your /home folder.

    """
    download_cdc_db(db_folder, email)


if __name__ == "__main__":
    emmtyper_db()
