from django import forms

# from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


class RangeWidget(forms.MultiWidget):
    template_name = "datashow/widgets/range.html"

    def __init__(self, widget, *args, **kwargs):
        self.prefix = kwargs.pop("prefix", "")
        self.postfix = kwargs.pop("postfix", "")
        super().__init__(widgets=(widget, widget), *args, **kwargs)
        self.widgets_names = ["_min", "_max"]

    def decompress(self, value):
        return value

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["prefix"] = self.prefix
        ctx["postfix"] = self.postfix
        return ctx


class RangeField(forms.MultiValueField):
    default_error_messages = {
        "invalid_start": _("Enter a valid start value."),
        "invalid_end": _("Enter a valid end value."),
    }

    def __init__(
        self,
        field_class,
        min_value=None,
        max_value=None,
        prefix="",
        postfix="",
        widget=forms.TextInput,
        *args,
        **kwargs,
    ):
        if "initial" not in kwargs:
            kwargs["initial"] = ["", ""]

        fields = (
            field_class(
                min_value=min_value,
                max_value=max_value,
            ),
            field_class(
                min_value=min_value,
                max_value=max_value,
            ),
        )

        super().__init__(
            fields=fields,
            widget=RangeWidget(widget, prefix=prefix, postfix=postfix),
            *args,
            **kwargs,
        )

    def compress(self, data_list):
        if data_list:
            return [
                self.fields[0].clean(data_list[0]),
                self.fields[1].clean(data_list[1]),
            ]
        return None


class CommaSeparatedMultiChoiceField(forms.MultipleChoiceField):
    default_error_messages = {
        "invalid_start": _("Enter a valid start value."),
        "invalid_end": _("Enter a valid end value."),
    }

    def to_python(self, value):
        if value is None:
            return []
        value = value.split(",")
        return [str(val) for val in value]
