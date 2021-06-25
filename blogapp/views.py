from blogapp.models import BlogPost
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from .models import Comment
from .utils import tags_count, similar_posts

class BlogListView(generic.ListView):
    model = BlogPost
    template_name = "blogapp/blog.html"
    paginate_by = 5
    tag = None

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['tags_count'] = tags_count()      
        if self.tag != None:
            context['tag'] = self.tag
        return context

    def get_queryset(self):
        self.tag = self.kwargs.get('tag', None)
        if self.tag != None:
            return BlogPost.objects.filter(tags__code__in=[self.tag])[:5]   
        return BlogPost.objects.all()[:5]

class BlogPostView(generic.DetailView):
    model = BlogPost 
    template_name = "blogapp/post.html"  

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['similar_posts'] = similar_posts(self.object.id)
        return context
    
    def post(self, request, *args, **kwargs):
        # Process added comments
        self.object = self.get_object()
        if (request.method == "POST") and ('comment_form' in request.POST):
            # Saving added comment
            cform = CommentForm(request.POST)
            if cform.is_valid():
                comment = Comment(
                    post=self.object, 
                    author=cform.cleaned_data["author"],
                    email=cform.cleaned_data["email"], 
                    content=cform.cleaned_data["content"]
                )
                comment.save()
                kwargs={
                    'pk': kwargs['pk'],
                    'slug': kwargs['slug'],
                }
                return redirect(reverse("blogapp:post", kwargs=kwargs))
        return render(request, self.template_name, self.get_context_data())