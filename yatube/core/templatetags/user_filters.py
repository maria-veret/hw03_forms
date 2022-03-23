from django import template


register = template.Library()


@register.filter
def addclass(field: str, css: str) -> str:
    """Фильтр для добавления CSS-классов в теги."""
    return field.as_widget(attrs={'class': css})
