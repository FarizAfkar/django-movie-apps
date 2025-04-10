from django import template
register = template.Library()

@register.filter
def list_genre(value):
    result = ''
    for _ in value:
        result += f'{_}, '
    return result.strip(' ,')+'.'
