from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .settings import DATASHOW_STORAGE_BACKEND


def get_sqlite_file_storage_path(instance, filename):
    filename = instance.slug + ".db"
    return "datashow/sqlitefiles/{}".format(filename)


def select_storage():
    return storages[DATASHOW_STORAGE_BACKEND]


class AbstractDataset(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("The name of the dataset."),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("Unique slug for the dataset."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Description for the dataset, default rendered as Markdown/HTML!"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the dataset was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the dataset was last updated."),
    )
    public = models.BooleanField(
        default=True,
        verbose_name=_("Is public"),
        help_text=_("Indicates whether the dataset is publicly accessible."),
    )
    listed = models.BooleanField(
        default=True,
        verbose_name=_("Is listed"),
        help_text=_("Indicates whether the dataset is listed."),
    )
    sqlite_file = models.FileField(
        upload_to=get_sqlite_file_storage_path,
        storage=select_storage,
        verbose_name=_("SQLite File"),
        help_text=_("Upload the SQLite file for the dataset."),
    )
    version = models.IntegerField(
        default=1,
        verbose_name=_("Version"),
        help_text=_("The version number of the dataset."),
    )
    default_table = models.ForeignKey(
        "Table",
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name=_("Default Table"),
        help_text=_("The default table is displayed instead of a list of all tables."),
    )

    class Meta:
        abstract = True
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")
        ordering = ("updated_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("datashow:dataset-index", kwargs={"slug": self.slug})

    def clean(self):
        if self.default_table and self.default_table.dataset_id != self.pk:
            raise ValidationError(
                {"default_table": "Default table needs to be part of this dataset."}
            )


class Dataset(AbstractDataset):
    class Meta(AbstractDataset.Meta):
        abstract = False


class Table(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="tables",
        verbose_name=_("Dataset"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Internal name of the table."),
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=_("Slug"),
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Displayed label for the table."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Description for the dataset, default rendered as Markdown/HTML!"),
    )
    row_count = models.IntegerField(
        default=0,
        verbose_name=_("Row Count"),
        help_text=_("The number of rows in the table."),
    )
    visible = models.BooleanField(
        default=True,
        verbose_name=_("Visible"),
        help_text=_("Indicates whether the table is visible."),
    )
    row_label_template = models.CharField(
        _("Row label template"),
        max_length=512,
        blank=True,
        help_text=_("Python format template for labeling rows."),
    )
    row_description_template = models.TextField(
        _("Row description template"),
        blank=True,
        help_text=_(
            "Python format template for describing rows / rendered as Markdown/HTML!"
        ),
    )
    primary_key = models.ForeignKey(
        "Column",
        verbose_name=_("Primary Key Column"),
        help_text=_("For use in identifying rows in URLs."),
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    pagination_size = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Pagination Size"),
        help_text=_("The number of rows per page."),
    )
    sql = models.TextField(
        _("SQL representation"),
        blank=True,
        help_text=_(
            "Makes this table 'virtual' by representing this table with this SQL query."
        ),
    )

    class Meta:
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["dataset", "slug"], name="unique_table_slug"
            ),
            models.UniqueConstraint(
                fields=["dataset", "name"], name="unique_table_name"
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.dataset.name})"

    def clean(self):
        if self.primary_key and self.primary_key.table_id != self.pk:
            raise ValidationError(
                _("Primary Key Column needs to be part of this table.")
            )
        example_row = {k: k for k in self.get_sql_columns()}
        try:
            self.row_label(example_row)
        except (KeyError, ValueError) as e:
            raise ValidationError(
                _("Row label template formatting error: %s") % e
            ) from e
        try:
            self.row_description(example_row)
        except (KeyError, ValueError) as e:
            raise ValidationError(
                _("Row description template formatting error: %s") % e
            ) from e

    def get_absolute_url(self):
        if self.dataset.default_table_id == self.pk:
            return self.dataset.get_absolute_url()
        return reverse(
            "datashow:dataset-table",
            kwargs={"slug": self.dataset.slug, "table_slug": self.slug},
        )

    def as_sql(self):
        """
        Table can be defined by a SQL query or by an actual table with that name.
        """
        if self.sql:
            return '({}) AS "{}"'.format(self.sql, self.name)
        return self.name

    def get_row_count(self):
        from .query import SqlQuery
        from .table import get_count

        query = SqlQuery(self, None).with_count()
        return get_count(self, query)

    def get_columns(self) -> list["Column"]:
        if not hasattr(self, "_columns"):
            self._columns = list(self.columns.all())
        return self._columns

    def get_visible_columns(self) -> list["Column"]:
        return [col for col in self.get_columns() if col.visible]

    def get_detail_visible_columns(self) -> list["Column"]:
        return [col for col in self.get_columns() if col.visible_detail]

    def get_filter_columns(self) -> list["Column"]:
        return [col for col in self.get_columns() if col.filter]

    def get_facet_columns(self) -> list["Column"]:
        return [col for col in self.get_columns() if col.facet_count]

    def get_sortable_columns(self) -> list["Column"]:
        return [col for col in self.get_columns() if col.sortable]

    def get_sql_columns(self) -> list[str]:
        return [col.name for col in self.get_columns()]

    def get_formatted_columns(self) -> list[dict]:
        from .formatters import format_column

        return [(c, format_column(c)) for c in self.get_visible_columns()]

    def has_fts(self):
        if not self.primary_key:
            return False
        return any(col.searchable for col in self.get_columns())

    def row_label(self, row: dict) -> str:
        try:
            return self.row_label_template.format(**row)
        except (KeyError, ValueError):
            return ""

    def row_description(self, row: dict) -> str:
        try:
            return self.row_description_template.format(**row)
        except (KeyError, ValueError):
            return ""


class FormatterChoices(models.TextChoices):
    PLAINTEXT = "plaintext", _("Plaintext")
    FLOAT = "float", _("Float")
    INTEGER = "integer", _("Integer")
    DATE = "date", _("Date")
    DATETIME = "datetime", _("Date and time")
    BOOLEAN = "boolean", _("Boolean")
    LINK = "link", _("Link")
    SUMMARY = "summary", _("Summary")
    ABBREVIATION = "abbreviation", _("Abbreviation")
    IFRAME = "iframe", _("IFrame")


class FilterChoices(models.TextChoices):
    ICONTAINS = "ilike", _("Substring")
    INTEGER_RANGE = "integer_range", _("Integer Range")


class NonStrippingCharField(models.CharField):
    """A TextField that does not strip whitespace at the beginning/end of
    it's value. Might be important for markup/code."""

    def formfield(self, **kwargs):
        kwargs["strip"] = False
        return super().formfield(**kwargs)


class Column(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="columns",
        verbose_name=_("Table"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Internal name of the column."),
    )
    label = models.CharField(
        max_length=255,
        verbose_name=_("Label"),
        help_text=_("Displayed label of the column."),
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name=_("Order"),
        help_text=_("Order of the column."),
    )
    visible = models.BooleanField(
        default=True,
        verbose_name=_("Visible"),
        help_text=_("Indicates whether the column is visible in table view."),
    )
    visible_detail = models.BooleanField(
        default=True,
        verbose_name=_("Visible in detail"),
        help_text=_("Indicates whether the column is visible in detail view."),
    )
    sortable = models.BooleanField(
        default=False,
        verbose_name=_("Sortable"),
        help_text=_("Indicates whether the column is sortable."),
    )
    searchable = models.BooleanField(
        default=False,
        verbose_name=_("Searchable"),
        help_text=_("Indicates whether the column is included in search queries."),
    )
    facet_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Facet Count"),
        help_text=_("Number of facet entries, 0 if disabled."),
    )
    prefix = NonStrippingCharField(
        max_length=255,
        blank=True,
        verbose_name=_("Prefix"),
        help_text=_("Prefix when outputting the column value."),
    )
    postfix = NonStrippingCharField(
        max_length=255,
        blank=True,
        verbose_name=_("Postfix"),
        help_text=_("Postfix when outputting the column value."),
    )
    formatter = models.CharField(
        choices=FormatterChoices.choices,
        max_length=255,
        default="plaintext",
        verbose_name=_("Formatter"),
        help_text=_("Formatter for the column."),
    )
    formatter_arguments = models.JSONField(
        blank=True,
        default=dict,
        verbose_name=_("Formatter Arguments"),
        help_text=_("Arguments for the formatter."),
    )
    filter = models.CharField(
        choices=FilterChoices.choices,
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("Filter"),
        help_text=_("Filter function for the column."),
    )
    filter_arguments = models.JSONField(
        blank=True,
        default=dict,
        verbose_name=_("Filter Arguments"),
        help_text=_("Arguments for the selected filter."),
    )

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        ordering = ("order",)
        constraints = [
            models.UniqueConstraint(
                fields=["table", "name"], name="unique_table_column_name"
            ),
        ]

    def __str__(self):
        return f"{self.label} - {self.table}"
