from django import template

register = template.Library()


@register.simple_tag
def strip_page(querystring):
    return querystring.split('&page')[0]


@register.simple_tag
def minus(a, b):
    return "{0:+.1f}".format(float(a) - float(b))


@register.simple_tag
def minus_percentage(percentage, value):
    return "{:+2d}".format(percentage - int(value * 10))


@register.simple_tag
def member_rating(rating_dict, member_name):
    if rating_dict[member_name] is not None:
        return rating_dict[member_name]
    else:
        return "?"


@register.simple_tag
def minus_member_rating(user_rating, rating_dict, member_name):
    if rating_dict[member_name] is not None:
        return "{0:+.1f}".format(float(user_rating) - float(rating_dict[member_name]))
    else:
        return "N/A"
