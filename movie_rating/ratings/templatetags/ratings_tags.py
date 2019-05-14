from django import template

register = template.Library()


@register.simple_tag
def strip_page(querystring):
    return querystring.split('&page')[0]
