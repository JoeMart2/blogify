"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, CommentCreateView, PostListAPIView, PostDetailAPIView, CreateCommentAPIView, CreatePostAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
    
    path('api/posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('api/post/<int:pk>/', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('api/post/<int:post_id>/comment/', CreateCommentAPIView.as_view(), name='api_comment_create'),
    path('api/create_post/', CreatePostAPIView.as_view(), name='api_create_post'),
]
