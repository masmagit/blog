from django.db import models
from django.urls import reverse
from userapp.models import Profile

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default='')
    image = models.ImageField(blank=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Profile)
    tags = models.ManyToManyField("Tag", blank=True)

    class Meta:
       ordering = ['-created']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:post', kwargs={'pk': self.id})

    @property
    def get_comments(self):
        return self.comments.all()

class Tag(models.Model):
    code = models.CharField(max_length=20)
    category = models.ManyToManyField("Category")

    def __str__(self) -> str:
        return self.code

class Category(models.Model):
    code = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.code

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, null=True, blank=True, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete = models.CASCADE)
    author = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')

    class Meta:
        ordering = ('created',)

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)