from blogapp.models import BlogPost
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

class BlogListView(generic.ListView):
    model = BlogPost
    queryset = BlogPost.objects.all()[:10]
    template_name = "blogapp/blog.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['tags_count'] = tags_count()
        return context

class BlogPostView(generic.DetailView):
    model = BlogPost 
    template_name = "blogapp/post.html"  

def tags_count():
    return BlogPost.objects.values('tags__code').annotate(Count('tags__code'))