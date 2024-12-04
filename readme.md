### API Endpoints for the Blog System

This guide provides an overview of the available API endpoints for the blog system, as well as usage instructions. The system supports both web and API-based views to manage blog posts, comments, and authors.

---

### **Web Endpoints** (Views rendered using Django Templates)

1. **`GET /posts/`** - List all published blog posts.
   - **URL**: `/posts/`
   - **Method**: `GET`
   - **Response**: Displays a list of published posts, showing the post titles and their associated authors.
   - **Template**: `post_list.html`

2. **`GET /post/<pk>/`** - View the details of a single post.
   - **URL**: `/post/<int:pk>/`
   - **Method**: `GET`
   - **Response**: Displays the full details of a specific post, including the content, title, author, and publication date.
   - **Template**: `post_detail.html`

3. **`POST /post/<post_id>/comment/`** - Create a comment for a specific post.
   - **URL**: `/post/<int:post_id>/comment/`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
         "content": "Your comment here"
     }
     ```
   - **Response**: Redirects to the post detail page upon successful comment creation.

---

### **API Endpoints** (For interacting with the system via REST)

1. **`GET /api/posts/`** - List all posts.
   - **URL**: `/api/posts/`
   - **Method**: `GET`
   - **Query Parameters** (optional):
     - `title`: Filter by post title.
     - `author_name`: Filter by author's name.
     - `published_date`: Filter by the published date.
   - **Response**: Returns a list of posts in JSON format.
     ```json
     [
         {
             "id": 1,
             "title": "Post 1",
             "content": "Content of post 1",
             "published_date": "2024-12-01T12:00:00Z",
             "author_name": "John Doe"
         },
         {
             "id": 2,
             "title": "Post 2",
             "content": "Content of post 2",
             "published_date": "2024-12-02T12:00:00Z",
             "author_name": "Jane Doe"
         }
     ]
     ```

2. **`GET /api/post/<pk>/`** - Get detailed information of a specific post.
   - **URL**: `/api/post/<int:pk>/`
   - **Method**: `GET`
   - **Response**: Returns the post's full details, including comments.
     ```json
     {
         "id": 1,
         "title": "Post 1",
         "content": "Content of post 1",
         "published_date": "2024-12-01T12:00:00Z",
         "author_name": "John Doe",
         "comments": [
             {
                 "id": 1,
                 "content": "Great post!",
                 "created": "2024-12-04T12:00:00Z"
             }
         ]
     }
     ```

3. **`POST /api/post/<post_id>/comment/`** - Create a comment for a specific post.
   - **URL**: `/api/post/<int:post_id>/comment/`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
         "content": "This is a comment on the post."
     }
     ```
   - **Response**: Returns the created comment data in JSON format.
     ```json
     {
         "id": 1,
         "content": "This is a comment on the post.",
         "created": "2024-12-04T12:00:00Z",
         "post": 1
     }
     ```

4. **`POST /api/create_post/`** - Create a new blog post.
   - **URL**: `/api/create_post/`
   - **Method**: `POST`
   - **Body**:
     ```json
     {
         "title": "New Post",
         "content": "This is the content of the new post.",
         "published_date": "2024-12-05T00:00:00Z",
         "author": 1  // ID of the author
     }
     ```
   - **Response**: Returns the created post data in JSON format.
     ```json
     {
         "id": 3,
         "title": "New Post",
         "content": "This is the content of the new post.",
         "published_date": "2024-12-05T00:00:00Z",
         "author": 1
     }
     ```


## Test Overview

This test suite is designed to test the functionality of the following API endpoints:

1. **POST List API** – `/api/posts/`
2. **POST Create API** – `/api/create_post/`
3. **POST Comment Create API** – `/api/post/{post_id}/comment/`

### Test Cases

---

### **1. `test_post_list_filtering`**

#### **Purpose**:
Test the functionality of filtering posts by title, author name, and published date.

#### **Setup**:
- Creates two authors: "John Doe" and "Bobby Nash."
- Creates three posts, two by "John Doe" and one by "Bobby Nash."

#### **Test Steps**:
- **Filter by Title**: Check if filtering by title returns only the post with the title "Post 1."
- **Filter by Author Name**: Check if filtering by author name "John Doe" returns two posts.
- **Filter by Published Date**: Check if filtering by an unavailable published date (e.g., `2024-01-01`) returns no posts.

#### **Expected Results**:
- When filtering by title, the response should contain only one post with the title `"Post 1"`.
- When filtering by `"author__name": "John Doe"`, the response should contain exactly 2 posts by this author.
- When filtering by an unavailable `published_date`, the response should return 0 posts.

---

### **2. `test_create_post`**

#### **Purpose**:
Test the ability to create a new post via the API.

#### **Setup**:
- Creates an author, "John Doe."

#### **Test Steps**:
- Sends a `POST` request with valid data (title, content, author) to `/api/create_post/` to create a new post.

#### **Expected Results**:
- The response should have a status code of `201 Created`.
- The returned post data should match the sent data, including the `title` ("New Post") and `author` ID.
  
---

### **3. `test_create_comment`**

#### **Purpose**:
Test the ability to create a comment on a post via the API.

#### **Setup**:
- Creates an author, "John Doe."
- Creates a post with the title "Test Post."

#### **Test Steps**:
- Sends a `POST` request to `/api/post/{post_id}/comment/` with a comment (`content`) for the specific post.

#### **Expected Results**:
- The response should have a status code of `201 Created`.
- The returned comment data should match the content (`"This is a comment"`) and be associated with the correct post ID.


## Test Output

### **Expected Failures/Successes**:

If a test fails, the assertion error message will be printed to help debug the issue. For example:

- **For `test_post_list_filtering`:**
  - If the filter on title does not return the correct post:
    ```
    AssertionError: Expected post with title 'Post 1', but got a different title.
    ```
  - If the filter by author name returns an incorrect number of posts:
    ```
    AssertionError: Expected 2 posts to be returned for 'John Doe'.
    ```

- **For `test_create_post`:**
  - If the response status code is not 201:
    ```
    AssertionError: Expected status code 201, got <actual status code> for creating a post.
    ```

- **For `test_create_comment`:**
  - If the comment content does not match:
    ```
    AssertionError: Expected comment content 'This is a comment', but got <actual content>.
    ```
