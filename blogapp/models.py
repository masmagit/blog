from django.db import models
from userapp.models import Profile

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Profile)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    code = models.CharField(max_length=20)
    category = models.ManyToManyField("Category")

    def __str__(self) -> str:
        return self.code

class Category(models.Model):
    code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.code