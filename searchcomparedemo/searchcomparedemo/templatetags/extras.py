from django import template
register = template.Library()
    
def get_item(dictionary, key):
    if dictionary in (None,'') or key not in dictionary:
        return 0 
    count = dictionary.get(key)
    if count == None:
        return 0
    return round(float(dictionary.get(key)),2)

register.filter('get_item',get_item)