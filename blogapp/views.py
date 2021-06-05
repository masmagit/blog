from blogapp.models import BlogPost
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class BlogListView(generic.ListView):
    model = BlogPost
    queryset = BlogPost.objects.all()[:10]
    template_name = "blogapp/blog.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['user'] = BlogPost.objects.all().first().authors.first().user
        return context

def post(request):
    return render(request, "blogapp/post.html")