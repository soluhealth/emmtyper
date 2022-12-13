import datetime
import json
import pathlib
from emmtyper.utilities import make_db


db_hist = json.loads('[{"updated_on": "2019-08-15", "host": "ftp.cdc.gov", "filename": "/pub/infectious_diseases/biotech/tsemm/trimmed.tfa", "uploaded_to_server_on": "2019-08-13"}, \
                    {"updated_on": "2020-10-01", "host": "ftp.cdc.gov", "filename": "/pub/infectious_diseases/biotech/tsemm/trimmed.tfa", "uploaded_to_server_on": "2020-09-29"}]')


def test_load_db_history(tmp_path):
    db_hist_path = tmp_path / "db_hist.json"
    with open(db_hist_path, "w") as db_hist_file:
        json.dump(db_hist, db_hist_file)
    db_instance = make_db.DBMetadata(db_hist_path, "email@example.com")

    assert db_instance.metad["updated_on"] == datetime.datetime(2020, 10, 1, 0, 0)
    assert db_instance.metad["host"] == "ftp.cdc.gov"
    assert db_instance.metad["filename"] == "/pub/infectious_diseases/biotech/tsemm/trimmed.tfa"
    assert db_instance.metad["uploaded_to_server_on"] == datetime.datetime(2020, 9, 29, 0, 0)

def test_update_history(tmp_path):
    db_hist_path = tmp_path / "db_hist.json"
    with open(db_hist_path, "w") as db_hist_file:
        json.dump(db_hist, db_hist_file)
    db_instance = make_db.DBMetadata(db_hist_path, "email@example.com")
    db_instance.update_info("updated_on", datetime.datetime(2021, 3, 3, 0, 0))
    db_instance.update_info("uploaded_to_server_on", datetime.datetime(2021, 3, 1, 0, 0))
    db_instance.update_metadata_file()
    with open(db_hist_path) as db_hist_file:
        db_hist_new = json.load(db_hist_file, object_hook=make_db.decode_history)
    assert len(db_hist_new) == 3
    assert db_hist_new[-1]["updated_on"] == datetime.datetime(2021, 3, 3, 0, 0)
    assert db_hist_new[-1]["uploaded_to_server_on"] == datetime.datetime(2021, 3, 1, 0, 0)

def test_make_db(tmp_path):
    fasta = tmp_path / "trimmed.tfa"
    local_fasta = pathlib.Path(__file__).parent / "8Jun17.fasta"
    fasta.write_bytes(local_fasta.read_bytes())
    db_instance = make_db.DBMetadata(tmp_path / "db_hist.json", "email@example.com")
    db_instance.make_db(fasta)
    db_instance.update_metadata_file()
    p = [p.name for p in pathlib.Path(tmp_path).glob("*.tfa*")]
    assert 'trimmed.tfa.clean' in p
    assert 'trimmed.tfa.ndb' in p 
    assert 'trimmed.tfa.nhr' in p
    assert 'trimmed.tfa' in p
    assert 'trimmed.tfa.nto' in p
    assert 'trimmed.tfa.ntf' in p
    assert 'trimmed.tfa.not' in p
    assert 'trimmed.tfa.nsq' in p
    assert 'trimmed.tfa.nin' in p
    with open(tmp_path / "db_hist.json") as db_hist_file:
        db_hist_new = json.load(db_hist_file, object_hook=make_db.decode_history)
    assert len(db_hist_new) == 1
    assert db_hist_new[-1]['total_seqs'] == 1819
    assert db_hist_new[-1]['total_duplicate_seqs'] == 7
