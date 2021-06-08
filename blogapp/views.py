from blogapp.models import BlogPost
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .forms import CommentForm
from .models import Comment

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

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (request.method == "POST") and ('comment_form' in request.POST):
            cform = CommentForm(request.POST)
            if cform.is_valid():
                comment = Comment(
                    post=self.object, 
                    author=cform.cleaned_data["author"], 
                    email=cform.cleaned_data["email"],
                    content=cform.cleaned_data["content"]
                )
                comment.save()
                return redirect(reverse("blogapp:post", kwargs={'pk': kwargs['pk']}))
        context = {}
        return render(request, self.template_name, self.get_context_data())


def tags_count():
    return BlogPost.objects.values('tags__code').annotate(Count('tags__code'))