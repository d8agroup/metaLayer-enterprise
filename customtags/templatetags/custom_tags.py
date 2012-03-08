from django import template
import re
from companies.utils import user_is_company_admin

register = template.Library()
 
@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
 
    truncd_val = value[:max_length]
    #if value[max_length] != " ":
        #rightmost_space = truncd_val.rfind(" ")
        #if rightmost_space != -1:
            #truncd_val = truncd_val[:rightmost_space]
 
    return truncd_val + "..."

@register.filter('is_url')
def is_url(value):
    return re.search('http', value)

@register.filter('is_in')
def is_in(value, list):
    return value in list

@register.filter('is_company_admin')
def is_company_admin(user, company):
    return user_is_company_admin(user, company)

@register.filter('is_true')
def is_true(value):
    return value == True or value == 'True'