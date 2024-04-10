from django.template import Library

register = Library()


@register.filter
def to_list(value, ):
    return range(int(value))