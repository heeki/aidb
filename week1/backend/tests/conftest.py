import tempfile
import pathlib
import os
import backend.database as db_mod

_original_db = db_mod.DB_PATH
_tmp_file = None


def get_test_db():
    global _tmp_file
    if _tmp_file is None:
        _tmp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        _tmp_file.close()
    return pathlib.Path(_tmp_file.name)


def pytest_configure(config):
    db_mod.DB_PATH = get_test_db()
    db_mod.reset_engine()
    db_mod.init_db()


def pytest_unconfigure(config):
    global _tmp_file
    db_mod.reset_engine()
    db_mod.DB_PATH = _original_db
    if _tmp_file:
        os.unlink(_tmp_file.name)
        _tmp_file = None
