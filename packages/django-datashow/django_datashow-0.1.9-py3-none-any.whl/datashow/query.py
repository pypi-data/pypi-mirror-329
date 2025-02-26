import re
from typing import Optional

from .forms import SEARCH_PARAM, SORT_PARAM
from .models import FilterChoices

NONE_VALUE = "-"
SEP = re.compile(r'\s+|(".*?")')
MIN_WORD_PREFIX_LENGTH = 3
PREFIX_QUERY_MARKER = "*"


def make_fts_query(q: str) -> str:
    if q.count('"') % 2:
        q += '"'
    query = []
    for p in (x for x in SEP.split(q) if x and x != '""'):
        if '"' not in p and len(p) >= MIN_WORD_PREFIX_LENGTH:
            p = f'"{p}"*'
        elif '"' not in p:
            p = f'"{p}"'
        query.append(p)
    return " ".join(query)


class SqlQuery:
    def __init__(self, table, formdata: Optional[dict] = None):
        self.table = table
        self.column_map = {col.name: col for col in table.get_columns()}
        self.select = []
        self._from = [self.table.as_sql()]
        self.where = []
        self.groupby = []
        self.order = []
        self.limit = None
        self.offset = None
        self.params = []
        self.formdata = formdata

    def __str__(self) -> str:
        return "{} {}".format(self.to_sql(), self.params)

    def add_select(self):
        self.select = [
            '"{table}"."{col}" AS "{col}"'.format(table=self.table.name, col=col)
            for col in self.table.get_sql_columns()
        ]

    def add_limit(self, page_slice):
        if page_slice:
            self.limit = page_slice.stop - (page_slice.start or 0)
            self.offset = page_slice.start or 0
        else:
            self.limit = self.table.pagination_size

    def with_list(self, page_slice=None):
        self.add_select()
        self.add_filter()
        self.add_order()
        self.add_limit(page_slice)
        return self

    def with_all(self):
        self.add_select()
        self.add_filter()
        self.add_order()
        return self

    def with_count(self):
        self.select = ["COUNT(*)"]
        self.add_filter()
        return self

    def with_row(self, row_id):
        self.add_select()
        self.where.append(
            '"{table}"."{pk_col}" = ?'.format(
                table=self.table.name, pk_col=self.table.primary_key.name
            )
        )
        self.params.append(row_id)
        return self

    def with_facet(self, column):
        self.select = [
            '"{table}"."{col}" AS key, COUNT(*) AS count'.format(
                table=self.table.name, col=column.name
            )
        ]
        self.add_filter(exclude_column=column.name)
        self.limit = column.facet_count
        if column.sortable:
            self.order = ["key ASC"]
        else:
            self.order = ["count DESC"]
        self.groupby = ["key"]
        return self

    def to_sql(self) -> str:
        return "SELECT {select} FROM {from_} {where} {groupby} {order} {limit} {offset}".format(
            select=", ".join(self.select),
            # join JOINs with space
            from_=" ".join(self._from),
            where="WHERE " + " AND ".join(self.where) if self.where else "",
            groupby="GROUP BY " + ", ".join(self.groupby) if self.groupby else "",
            order="ORDER BY " + ", ".join(self.order) if self.order else "",
            limit="LIMIT {}".format(self.limit) if self.limit else "",
            offset="OFFSET {}".format(self.offset) if self.offset else "",
        )

    def add_order(self):
        if not self.formdata:
            return
        sort_columns = self.formdata.get(SORT_PARAM, [])
        for sort in sort_columns:
            direction = "ASC"
            if sort.startswith("-"):
                direction = "DESC"
                sort = sort[1:]
            if sort not in self.column_map:
                continue
            if not self.column_map[sort].sortable:
                continue
            self.order.append(
                '"{table}"."{col}" {dir}'.format(
                    table=self.table.name, col=sort, dir=direction
                )
            )

    def add_filter(self, exclude_column=None):
        if not self.formdata:
            return
        filter_columns = self.table.get_filter_columns()
        filter_columns = [col for col in filter_columns if col.name != exclude_column]
        facet_columns = self.table.get_facet_columns()
        facet_columns = [col for col in facet_columns if col.name != exclude_column]

        query: str = self.formdata.get(SEARCH_PARAM)
        if query and self.table.has_fts():
            query = make_fts_query(query)
            fts_table_name = f"{self.table.name}__fts"
            pk_col = self.table.primary_key.name
            self._from.append(
                f'JOIN "{fts_table_name}" ON "{self.table.name}"."{pk_col}" = "{fts_table_name}"."{pk_col}"'
            )
            self.where.append(f"{fts_table_name} MATCH ?")
            self.params.append(query)

        for column in facet_columns:
            value = self.formdata.get(column.name)
            if value:
                if value == NONE_VALUE:
                    self.where.append(f'"{self.table.name}"."{column.name}" IS NULL')
                else:
                    self.where.append(f'"{self.table.name}"."{column.name}" = ?')
                    self.params.append(value)

        for column in filter_columns:
            column_filter = column.filter
            if column_filter == FilterChoices.INTEGER_RANGE:
                field_value = self.formdata.get(column.name + "__range")
                if field_value is None:
                    continue
                min_value, max_value = field_value
                if min_value is not None and max_value is not None:
                    self.where.append(
                        f'"{self.table.name}"."{column.name}" BETWEEN ? AND ?'
                    )
                    self.params.extend([min_value, max_value])
                elif min_value is not None:
                    self.where.append(f'"{self.table.name}"."{column.name}" >= ?')
                    self.params.append(min_value)
                elif max_value is not None:
                    self.where.append(f'"{self.table.name}"."{column.name}" <= ?')
                    self.params.append(max_value)
