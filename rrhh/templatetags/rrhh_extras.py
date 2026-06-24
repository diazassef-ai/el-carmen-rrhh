from django import template


register = template.Library()


@register.filter
def has_group(user, group_name):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


@register.filter
def has_any_group(user, group_names):
    if not user.is_authenticated:
        return False
    names = [name.strip() for name in group_names.split(",")]
    return user.groups.filter(name__in=names).exists()
