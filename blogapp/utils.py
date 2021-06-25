from django.db.models import Count
from .models import Tag, BlogPost

def tags_count():
    return Tag.objects.values('code').annotate(posts_count=Count('blogposts'))

def similar_posts(post_id:int):
    post_tags_ids = BlogPost.objects.get(id=post_id).tags.values_list('id', flat=True)
    simposts = BlogPost.objects.filter(tags__in=post_tags_ids).exclude(id=post_id)
    simposts = simposts.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:5]
    return simposts