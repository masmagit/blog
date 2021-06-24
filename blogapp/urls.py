from django.conf.urls import url
from django.urls import path
from . import views

app_name = "blogapp"
urlpatterns = [
    path('', views.BlogListView.as_view(), name="blog"),
    path('tag/<str:tag>/', views.BlogListView.as_view(), name="blog_tag"),
    path('post/<int:pk>-<str:slug>/', views.BlogPostView.as_view(), name="post"),
]