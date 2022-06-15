from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag("search_bar.html", takes_context=True)
def render_search_bar(context):
    return {
        "selected_category": context.get("selected_category"),
        "selected_keyword": context.get("selected_keyword", ""),
        "fetched_categories": Category.objects.all()
    }
