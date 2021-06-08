from django.contrib import admin
from userapp.models import Profile
from .models import BlogPost, Tag, Category, Comment

admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
