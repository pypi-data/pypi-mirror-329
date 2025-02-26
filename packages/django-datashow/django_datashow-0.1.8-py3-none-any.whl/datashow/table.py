import logging
import sqlite3
from typing import Generator, NamedTuple, Optional

from django.utils.text import slugify

from .db import open_cursor, open_write_cursor
from .formatters import format_value
from .models import Column, Dataset, Table
from .query import NONE_VALUE, SqlQuery

logger = logging.getLogger(__name__)


class SqliteColumn(NamedTuple):
    name: str
    type: str
    notnull: int
    default: str
    pk: int


class SqliteTableData(NamedTuple):
    name: str
    columns: list[SqliteColumn]
    count: int


SQLITE_TYPE_FORMATTER_MAP = {
    "NULL": "plaintext",
    "INTEGER": "integer",
    "REAL": "float",
    "TEXT": "plaintext",
    "BLOB": "plaintext",
}


class FacetEntry(NamedTuple):
    key: str
    count: int
    active: bool


class Facet(NamedTuple):
    column: Column
    keys: list[FacetEntry]


def get_facets(table: Table, formdata: Optional[dict]) -> list[Facet]:
    facet_cols = [col for col in table.get_columns() if col.facet_count]
    facets = []
    for column in facet_cols:
        query = SqlQuery(table, formdata).with_facet(column)
        active_value = None
        if formdata and column.name in formdata:
            active_value = str(formdata[column.name])
        counts = list(get_facet_counts(table, query, active_value))
        facets.append(Facet(column, counts))
    return facets


class RowQueryset:
    def __init__(self, table: Table, formdata):
        self.table = table
        self.formdata = formdata
        self._rows = []

    def count(self):
        query = SqlQuery(self.table, self.formdata).with_count()
        if not query.params:
            if not self.table.row_count:
                self.table.row_count = get_count(self.table, query)
                if self.table.row_count:
                    self.table.save(update_fields=["row_count"])
            return self.table.row_count
        return get_count(self.table, query)

    def stream_raw(self, chunk_size=1000):
        query = SqlQuery(self.table, self.formdata).with_all()
        return get_raw_rows_iter(self.table, query, chunk_size)

    def __getitem__(self, page_slice):
        # Evaluate on slice
        query = SqlQuery(self.table, self.formdata).with_list(page_slice=page_slice)
        self._rows = get_rows(self.table, query)
        return self

    def __iter__(self):
        return iter(self._rows)


def get_table_info(cursor, table_name: str) -> SqliteTableData:
    cursor.execute("PRAGMA table_info({})".format(table_name))
    columns = [SqliteColumn(*t[1:]) for t in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
    row_count = cursor.fetchone()[0]

    return SqliteTableData(name=table_name, columns=columns, count=row_count)


def get_sqlite_table_data(dataset: Dataset) -> list[SqliteTableData]:
    with open_cursor(dataset) as cursor:
        cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
        sqlite_tables = cursor.fetchall()
        filtered_sqlite_tables = [
            table[1]
            for table in sqlite_tables
            if not table[1].endswith("__fts") and "__fts_" not in table[1]
        ]
        return [get_table_info(cursor, table) for table in filtered_sqlite_tables]


def initialize_dataset(dataset: Dataset):
    for sqlite_table_data in get_sqlite_table_data(dataset):
        table, _created = Table.objects.get_or_create(
            dataset=dataset,
            name=sqlite_table_data.name,
            defaults={
                "slug": slugify(sqlite_table_data.name),
                "label": sqlite_table_data.name,
                "row_count": sqlite_table_data.count,
            },
        )
        existing_columns = set(
            Column.objects.filter(table=table).values_list("name", flat=True)
        )
        incoming_columns = set(col.name for col in sqlite_table_data.columns)
        obsolete_columns = existing_columns - incoming_columns
        Column.objects.filter(table=table, name__in=obsolete_columns).delete()

        pk_col = None
        for i, sqlite_column in enumerate(sqlite_table_data.columns):
            column, _created = Column.objects.get_or_create(
                table=table,
                name=sqlite_column.name,
                defaults={
                    "label": sqlite_column.name.capitalize(),
                    "formatter": SQLITE_TYPE_FORMATTER_MAP.get(
                        sqlite_column.type, "plaintext"
                    ),
                    "order": i,
                },
            )
            if sqlite_column.pk and not pk_col:
                pk_col = column
        if pk_col:
            table.primary_key = column
            table.save(update_fields=["primary_key"])


class RenderRow(NamedTuple):
    value: str
    css: str
    formatted_value: str
    column: Column


def format_column_value(row_data, column: Column, detail=False) -> RenderRow:
    value = row_data[column.name]
    css, formatted_value = format_value(column, value, row_data, detail=detail)
    return RenderRow(value, css, formatted_value, column)


def get_count(table: Table, query: SqlQuery):
    try:
        with open_cursor(table.dataset) as cursor:
            cursor.execute(query.to_sql(), query.params)
            return cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        logger.error("Error getting count: %s with %s", e, query)
        return 0


def get_facet_counts(
    table: Table, query: SqlQuery, active_value: Optional[str] = None
) -> Generator[FacetEntry, None, None]:
    try:
        with open_cursor(table.dataset) as cursor:
            cursor.execute(query.to_sql(), query.params)
            for row in cursor.fetchall():
                key = row[0]
                count = row[1]
                if key is None:
                    key = NONE_VALUE
                else:
                    key = str(key)
                yield FacetEntry(key, count, key == active_value)
    except sqlite3.OperationalError as e:
        logger.error("Error getting facet count: %s with %s", e, query)
        return 0


def get_rows(table: Table, query: SqlQuery) -> list[list[RenderRow]]:
    dataset = table.dataset
    col_list = table.get_sql_columns()
    try:
        with open_cursor(dataset) as cursor:
            cursor.execute(query.to_sql(), query.params)
            rows = cursor.fetchall()
            # Fetch all data
            row_list = [
                dict([(col, val) for col, val in zip(col_list, row)]) for row in rows
            ]
            # Format with complete row data
            # but return only visible columns
            return [
                [
                    format_column_value(row_data, col)
                    for col in table.get_visible_columns()
                ]
                for row_data in row_list
            ]
    except sqlite3.OperationalError as e:
        logger.error("Error getting rows: %s with %s", e, query)
        return []


def get_raw_rows_iter(
    table: Table, query: SqlQuery, chunk_size=1000
) -> Generator[dict, None, None]:
    dataset = table.dataset
    try:
        with open_cursor(dataset) as cursor:
            cursor.execute(query.to_sql(), query.params)
            while True:
                rows = cursor.fetchmany(chunk_size)
                if not rows:
                    break
                for row in rows:
                    yield [str(val) if val is not None else "" for val in row]
    except sqlite3.OperationalError as e:
        logger.error("Error getting rows: %s", e)
        return []


def get_row(table: Table, row_id: str) -> tuple[list[RenderRow], dict]:
    col_list = table.get_sql_columns()
    with open_cursor(table.dataset) as cursor:
        query = SqlQuery(table).with_row(row_id)
        cursor.execute(query.to_sql(), query.params)
        row = cursor.fetchone()
        if not row:
            raise KeyError("Row not found")
        row_data = dict([(col, val) for col, val in zip(col_list, row)])
        # Return only visible columns
        return (
            [
                format_column_value(row_data, col, detail=True)
                for col in table.get_detail_visible_columns()
            ],
            row_data,
        )


def setup_fts(table: Table):
    with open_write_cursor(table.dataset) as cursor:
        setup_fts_with_cursor(cursor, table)


def setup_fts_with_cursor(cursor, table: Table) -> None:
    if not table.has_fts():
        return
    fts_columns = [col.name for col in table.get_columns() if col.searchable]
    fts_table_name = f"{table.name}__fts"
    pk_col = table.primary_key.name
    all_fts_columns = [pk_col] + fts_columns

    cursor.execute(
        "DROP TABLE IF EXISTS {}".format(fts_table_name),
    )
    cursor.execute(
        "CREATE VIRTUAL TABLE {} USING FTS5({})".format(
            fts_table_name, ", ".join(all_fts_columns)
        )
    )
    cursor.execute(
        "INSERT INTO {}({}) SELECT {} FROM {}".format(
            fts_table_name,
            ", ".join(all_fts_columns),
            ", ".join(all_fts_columns),
            table.as_sql(),
        )
    )
