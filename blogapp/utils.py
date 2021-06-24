from django.db.models import Count
from .models import Tag, BlogPost

def tags_count():
    return Tag.objects.values('code').annotate(posts_count=Count('blogposts'))