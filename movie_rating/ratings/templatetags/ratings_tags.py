from django import template

register = template.Library()


@register.simple_tag
def strip_page(querystring):
    return querystring.split('&page')[0]


@register.simple_tag
def minus(a, b):
    return "{0:+.1f}".format(float(a) - float(b))


@register.simple_tag
def minus_percentage(value, percentage):
    return "{:+2d}".format(int(value * 10) - percentage)
