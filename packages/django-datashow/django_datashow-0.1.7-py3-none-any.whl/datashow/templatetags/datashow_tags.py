import markdown
from django import template
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

from ..forms import SORT_PARAM

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, key=None, value=None):
    request = context["request"]
    if key is None:
        return request.META["QUERY_STRING"]
    if value is None:
        query = request.GET.copy()
        query.pop(key, None)
        return query.urlencode()
    if request.GET.get(key) == value:
        return ""

    query = request.GET.copy()
    query[key] = value
    return query.urlencode()


@register.simple_tag(takes_context=True)
def sort_queryparam(context, column, ascending=True, remove=False):
    request = context["request"]
    current_value = request.GET.get(SORT_PARAM, "")
    value = column if ascending else "-" + column

    values_set = dict.fromkeys(x for x in current_value.split(",") if x)
    if not remove and value in values_set:
        return ""

    if remove:
        value = ",".join(x for x in values_set if x != value)
    else:
        values = [x for x in values_set if x != column and x[1:] != column]
        values.append(value)
        value = ",".join(values)

    query = request.GET.copy()
    if not value:
        query.pop(SORT_PARAM, None)
    else:
        query[SORT_PARAM] = value
    return query.urlencode()


@register.filter(name="listify")
def listify(value):
    return list(value)


@register.filter(name="markdownify")
def markdownify(value):
    return mark_safe(markdown.markdown(force_str(value)))
