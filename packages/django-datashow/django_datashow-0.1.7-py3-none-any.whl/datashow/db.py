import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path

from django.core.files.base import ContentFile

from .models import Dataset
from .settings import DATASHOW_DB_CACHE_PATH


def get_database_filename(dataset: Dataset) -> str:
    return "datashow-dataset-{}-{}.db".format(dataset.id, dataset.version)


def get_database_file(dataset: Dataset) -> Path:
    filename = get_database_filename(dataset)
    if DATASHOW_DB_CACHE_PATH is None:
        base_path = Path(tempfile.gettempdir())
    else:
        base_path = Path(DATASHOW_DB_CACHE_PATH)

    filepath = base_path / filename
    if filepath.exists():
        return filepath

    base_path.mkdir(exist_ok=True)

    with dataset.sqlite_file.open("rb") as sqlite_file:
        with open(filepath, "wb") as cache_file:
            cache_file.write(sqlite_file.read())

    return filepath


def get_database_connection(dataset: Dataset):
    filepath = get_database_file(dataset)
    return sqlite3.connect("file:{}?mode=ro".format(filepath), uri=True)


@contextmanager
def open_db(dataset):
    connection = get_database_connection(dataset)
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def open_cursor(dataset):
    with open_db(dataset) as connection:
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()


@contextmanager
def open_write_cursor(dataset: Dataset):
    filepath = get_database_file(dataset)
    connection = sqlite3.connect(
        "file:{}".format(filepath), uri=True, isolation_level="EXCLUSIVE"
    )
    assert not connection.in_transaction
    try:
        cursor = connection.cursor()

        cursor.execute("PRAGMA JOURNAL_MODE = DELETE;")
        # Smaller page size for better performance when using HTTP range requests
        cursor.execute("PRAGMA page_size = 1024;")
        yield cursor
    finally:
        cursor.execute("COMMIT;")
        cursor.execute("VACUUM;")
        connection.commit()
        connection.close()

    # Write database back to origin and update version
    with open(filepath, "rb") as cache_file:
        new_sqlite = ContentFile(cache_file.read())
    dataset.version += 1
    filename = get_database_filename(dataset)
    dataset.sqlite_file.save(filename, new_sqlite, save=True)
