from rest_framework import serializers
from .models import Post, Comment, Author

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'content', 'created',]

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author_name', 'comments']

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
