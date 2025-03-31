from django import template
register = template.Library()
import re


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def video_embed(url):
    regex = r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)'
    match = re.search(regex, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return ""