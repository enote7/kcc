# Put this code in a file named 'custom_filters.py' in your app's directory
from django import template

register = template.Library()

@register.filter
def get_billing_service_choice(choices_dict, choice_key):
    return choices_dict.get(choice_key, 'Unknown')
