from django import template

register = template.Library()


@register.filter("is_manager")
def is_manager(user):
    if user.is_superuser:
        return True

    groups = user.groups.all().values_list("name", flat=True)
    return True if "manager" in groups else False
