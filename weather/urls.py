from django.urls import path
from . import views
from django.shortcuts import render
from .views import (PostListView,
                    MainPageListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView)


urlpatterns = [
    path('user/<str:username>', UserPostListView.as_view(template_name='user_postlist.html'),
         name='userpost_list'),
    path('allposts/', PostListView.as_view(template_name='postpage_list.html'),
         name='postpage_list'),
    path('', MainPageListView.as_view(
        template_name='extended_mainpage.html'), name='mainpage'),
    path('post/<int:pk>/', PostDetailView.as_view(template_name='post_detail.html'),
         name='post_details'),
    path('post/<int:pk>/update', PostUpdateView.as_view(template_name='post_create.html'),
         name='post_update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(template_name='post_delete.html'),
         name='post_delete'),
    path('post/new/', PostCreateView.as_view(template_name='post_create.html'),
         name='post_create'),
    path('index/', views.index, name='index'),
    path('project/', lambda request: render(request,
                                            'extended_project.html'), name='project'),
]
