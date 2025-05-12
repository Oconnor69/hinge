from django import template

register = template.Library()

@register.filter
def filter_by_status(candidatures, status):
    """
    Filtre une liste de candidatures par leur statut
    Usage: {{ candidatures|filter_by_status:'EN_ATTENTE' }}
    """
    return [c for c in candidatures if c.statut == status] 