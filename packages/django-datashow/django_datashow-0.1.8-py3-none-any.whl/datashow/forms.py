from django import forms
from django.utils.translation import gettext_lazy as _

from .fields import CommaSeparatedMultiChoiceField, RangeField
from .models import FilterChoices

SEARCH_PARAM = "q"
SORT_PARAM = "sort"


class FilterForm(forms.Form):
    def __init__(self, table, *args, **kwargs):
        self.table = table
        super().__init__(*args, **kwargs)
        sortable_columns = [col.name for col in self.table.get_sortable_columns()]
        if sortable_columns:
            self.fields[SORT_PARAM] = CommaSeparatedMultiChoiceField(
                label=_("Sort by"),
                choices=[("", "0")]
                + [(col, col) for col in sortable_columns]
                + [("-" + col, "-" + col) for col in sortable_columns],
                required=False,
                widget=forms.HiddenInput,
            )
        self.set_facet_fields()
        self.set_filter_fields()

    def set_facet_fields(self):
        facet_columns = self.table.get_facet_columns()
        for column in facet_columns:
            self.fields[column.name] = forms.CharField(
                label=column.label,
                required=False,
                widget=forms.HiddenInput(),
            )

    def set_filter_fields(self):
        if self.table.has_fts():
            self.fields[SEARCH_PARAM] = forms.CharField(
                label=_("Search term"),
                required=False,
                widget=forms.TextInput(attrs={"class": "form-control"}),
            )
        filter_columns = self.table.get_filter_columns()
        for column in filter_columns:
            column_filter = column.filter
            if column_filter == FilterChoices.INTEGER_RANGE:
                field_name = column.name + "__range"
                self.fields[field_name] = RangeField(
                    forms.IntegerField,
                    label=column.label,
                    min_value=column.filter_arguments.get("min"),
                    max_value=column.filter_arguments.get("max"),
                    prefix=column.prefix,
                    postfix=column.postfix,
                    required=False,
                    widget=forms.TextInput(
                        attrs={
                            "class": "form-control text-end",
                            "inputmode": "numeric",
                            "type": "number",
                            "min": column.filter_arguments.get("min", ""),
                            "max": column.filter_arguments.get("max", ""),
                        }
                    ),
                )

    def has_filter(self):
        return any(k for k in self.fields.keys() if k != SORT_PARAM)

    def is_filtered(self):
        if not self.is_valid():
            return False
        return any(v for k, v in self.cleaned_data.items() if k != SORT_PARAM)
