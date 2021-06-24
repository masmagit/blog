from django.db import models
from django.urls import reverse
from userapp.models import Profile
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Profile, related_name='blogposts')
    tags = models.ManyToManyField("Tag", blank=True, related_name='blogposts')
    slug = models.SlugField(max_length=100, blank=True, unique_for_date='created')

    class Meta:
       ordering = ['-created']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        kwargs={
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('blogapp:post', kwargs=kwargs)

    def save(self, *args, **kwargs):
        val = self.title
        self.slug = slugify(val, True)
        super().save(*args, **kwargs)

    @property
    def get_comments(self):
        return self.comments.all()

class Tag(models.Model):
    code = models.CharField(max_length=20)
    category = models.ManyToManyField("Category", related_name='tags')

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
    content = models.TextField()

    class Meta:
        ordering = ('created',)

    def __str__(self) -> str:
        return f'Comment by {self.author}, created on {self.created}'    

    def get_comments(self):
        return Comment.objects.filter(parent=self)