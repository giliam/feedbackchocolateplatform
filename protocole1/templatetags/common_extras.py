from django import template

from protocole1.models import Reactions

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, list) or isinstance(dictionary, tuple):
        return dictionary[key]
    else:
        return dictionary.get(key)


@register.filter
def conv_reaction(reaction):
    return str(Reactions(reaction).name)
