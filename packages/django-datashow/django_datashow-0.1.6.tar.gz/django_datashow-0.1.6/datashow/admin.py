from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import Column, Dataset, Table
from .table import initialize_dataset, setup_fts


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "version", "public", "listed")
    list_filter = ("public", "listed")
    search_fields = ("name", "slug")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ("default_table",)
    actions = ["initialize_dataset"]

    def save_model(
        self, request: HttpRequest, obj: Dataset, form: ModelForm, change: bool
    ) -> None:
        super().save_model(request, obj, form, change)
        if not obj.tables.exists():
            initialize_dataset(obj)

    @admin.action(description=_("Initialize datasets"))
    def initialize_dataset(self, request: HttpRequest, queryset):
        for dataset in queryset:
            initialize_dataset(dataset)
        self.message_user(request, _("Datasets initialized."))


class ColumnInline(admin.StackedInline):
    model = Column
    extra = 0
    fields = (
        "label",
        "visible",
        "visible_detail",
        "sortable",
        "searchable",
        "facet_count",
        "prefix",
        "postfix",
        "formatter",
        "formatter_arguments",
        "filter",
        "filter_arguments",
    )
    ordering = ("order",)
    show_change_link = True


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    inlines = [ColumnInline]
    list_display = ("name", "dataset", "row_count", "visible")
    search_fields = ("name", "slug")
    raw_id_fields = ("primary_key",)
    save_on_top = True
    list_filter = ("dataset", "visible")
    actions = ["generate_fts"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "slug",
                    "label",
                    "description",
                    "visible",
                    "row_label_template",
                    "primary_key",
                    "pagination_size",
                )
            },
        ),
        (
            _("Advanced"),
            {
                "classes": ["collapse"],
                "fields": [
                    "name",
                    "sql",
                    "dataset",
                    "row_count",
                ],
            },
        ),
    )

    @admin.action(description=_("Generate FTS tables"))
    def generate_fts(self, request: HttpRequest, queryset):
        for table in queryset:
            setup_fts(table)


@admin.register(Column)
class ColumnAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ("name", "label")
    list_filter = ("table", "visible", "visible_detail", "sortable", "searchable")
    list_display = (
        "name",
        "label",
        "table",
        "visible",
        "visible_detail",
        "sortable",
        "searchable",
        "facet_count",
    )

    actions = [
        "make_visible",
        "make_invisible",
        "make_visible_detail",
        "make_invisible_detail",
        "make_sortable",
        "make_unsortable",
        "make_searchable",
        "make_unsearchable",
    ]

    @admin.action(description=_("Make visible"))
    def make_visible(self, request: HttpRequest, queryset):
        queryset.update(visible=True)

    @admin.action(description=_("Make invisible"))
    def make_invisible(self, request: HttpRequest, queryset):
        queryset.update(visible=False)

    @admin.action(description=_("Make visible_detail"))
    def make_visible_detail(self, request: HttpRequest, queryset):
        queryset.update(visible_detail=True)

    @admin.action(description=_("Make invisible_detail"))
    def make_invisible_detail(self, request: HttpRequest, queryset):
        queryset.update(visible_detail=False)

    @admin.action(description=_("Make sortable"))
    def make_sortable(self, request: HttpRequest, queryset):
        queryset.update(sortable=True)

    @admin.action(description=_("Make unsortable"))
    def make_unsortable(self, request: HttpRequest, queryset):
        queryset.update(sortable=False)

    @admin.action(description=_("Make searchable"))
    def make_searchable(self, request: HttpRequest, queryset):
        queryset.update(searchable=True)

    @admin.action(description=_("Make unsearchable"))
    def make_unsearchable(self, request: HttpRequest, queryset):
        queryset.update(searchable=False)
