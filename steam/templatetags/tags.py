## tags.py
from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter
def keyvalue(dict, key, default=None):
    return dict.get(key, default)


#
# @register.filter
# def todir(m):
#     return dir(m)