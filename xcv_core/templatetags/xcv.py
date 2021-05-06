from urllib.parse import urlencode

from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="max")
def fubar_max(value, maxvalue):
    return max(value, maxvalue)


@register.filter(name="strip")
def strip(value, stripchar):
    if type(value) is str:
        return value.strip(stripchar)
    else:
        return value


@register.filter(name="addstr")
def addstr(a, b):
    return '{}_{}'.format(a, b)


# https://stackoverflow.com/a/36288962/
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    [query.pop(kwarg) for kwarg in kwargs if kwarg in query]
    query.update(kwargs)
    return urlencode(query)


# https://stackoverflow.com/a/50630001/
@register.tag
def lineless(parser, token):
    nodelist = parser.parse(('endlineless',))
    parser.delete_first_token()
    return LinelessNode(nodelist)


class LinelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        input_str = self.nodelist.render(context)
        output_str = ''
        for line in input_str.splitlines():
            if line.strip():
                output_str = '\n'.join((output_str, line))
        return output_str
