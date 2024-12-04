import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from .models import Post, Author

@pytest.mark.django_db
def test_post_list_filtering():
    # Setup data
    author = Author.objects.create(name="John Doe", email="john@example.com")
    author2 = Author.objects.create(name="Bobby Nash", email="bobby@example.com")
    post1 = Post.objects.create(title="Post 1", content="Content 1", author=author, status="published")
    post2 = Post.objects.create(title="Post 2", content="Content 2", author=author, status="published")
    post3 = Post.objects.create(title="Post 3", content="Content 3", author=author2, status="published")
    
    # Initialize the API client
    client = APIClient()
    
    # Test filtering by title
    response = client.get('/api/posts/', {'title': 'Post 1'})

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} for title filter."
    assert len(response.data) == 1, "Expected exactly 1 post to be returned for title filter."
    assert response.data[0]['title'] == 'Post 1', "Expected post with title 'Post 1', but got a different title."

    # Test filtering by author_name

    response = client.get('/api/posts/', {'author__name': 'John Doe'})
    print(response.data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} for author_name filter."
    assert len(response.data) == 2, "Expected 2 posts to be returned for 'John Doe'."
    
    # Test filtering by published_date (assuming no posts have this date yet)
    response = client.get('/api/posts/', {'published_date': '2024-01-01'})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} for published_date filter."
    assert len(response.data) == 0, "Expected 0 posts for the given published date."

@pytest.mark.django_db
def test_create_post():
    # Setup data
    author = Author.objects.create(name="John Doe", email="john@example.com")
    
    # Initialize the API client
    client = APIClient()
    
    # Data for creating a new post
    data = {
        'title': 'New Post',
        'content': 'This is a new post.',
        'published_date': '2024-01-01',
        'author': author.id
    }
    
    # Post request to create a new post
    response = client.post('/api/create_post/', data)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code} for creating a post."
    assert response.data['title'] == 'New Post', f"Expected title 'New Post', but got {response.data['title']}."
    assert response.data['author'] == author.id, f"Expected Author ID: {author.id}, but got {response.data['author']}."

@pytest.mark.django_db
def test_create_comment():
    # Setup data
    author = Author.objects.create(name="John Doe", email="john@example.com")
    post = Post.objects.create(title="Test Post", content="Test Content", author=author, status="published")
    
    # Initialize the API client
    client = APIClient()
    
    # Data for creating a new comment
    data = {'content': 'This is a comment'}
    
    # Post request to create a comment on the specific post
    
    response = client.post(f'/api/post/{post.id}/comment/', data)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code} for creating a comment."
    assert response.data['content'] == 'This is a comment', f"Expected comment content 'This is a comment', but got {response.data['content']}."
    assert response.data['post_id'] == post.id, f"Expected post ID {post.id}, but got {response.data['post_id']}."

