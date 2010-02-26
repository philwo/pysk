from django import template

register = template.Library()

@register.filter(name="php_ini_value")
def php_ini_value(value):
    if value == True:
        return "On"
    elif value == False:
        return "Off"
    else:
        return value
