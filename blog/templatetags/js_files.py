from django import template
from django.templatetags.static import static
import os

register = template.Library()

@register.simple_tag
def load_js_files(directory):
    # Assuming that all JavaScript files are in the static/js directory
    js_files = []
    static_dir = os.path.join(os.path.dirname(__file__), 'static', directory)
    for filename in os.listdir(static_dir):
        if filename.endswith('.js'):
            js_files.append(static(f'{directory}/{filename}'))
    return js_files