from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CreatePostSerializer
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

# Post List View (For web)
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author')

# Post Detail View (For web)
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


# Comment Create View (For web)
class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        form.instance.post = Post.objects.get(id=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['title', 'author__name', 'published_date']
    ordering_fields = ['published_date']

# Post Detail API View with JSON Response
class PostDetailAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create Comment API View with JSON Response
class CreateCommentAPIView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Post API View with JSON Response
class CreatePostAPIView(APIView):
    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
