from django.template import Library

register = Library()


@register.filter
def to_list(value, ):
    return range(int(value))

@register.filter
def minus(value, num):
    return value - int(num)