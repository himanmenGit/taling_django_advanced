from django import template
from ..models import Category, RestaurantTable

register = template.Library()


@register.inclusion_tag("search_bar.html", takes_context=True)
def render_search_bar(context):
    return {
        "weekdays": RestaurantTable.Weekday.choices,
        "selected_category": context.get("selected_category"),
        "selected_keyword": context.get("selected_keyword", ""),
        "selected_weekday": context.get("selected_weekday"),
        "selected_start": context.get("selected_start", ""),
        "selected_end": context.get("selected_end", ""),
        "fetched_categories": Category.objects.all()
    }
