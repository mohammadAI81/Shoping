from django.template import Library

register = Library()


@register.filter
def to_list(value, ):
    return range(1, int(value) + 1)


@register.filter
def to_type(value, ):
    print(type(value))
