from django.urls import path
from .views import main_page_view, PostListView, get_post_detail, create_post, update_post, delete_post, get_category_posts, get_tag_posts

app_name = 'blog'

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path('posts/add/', create_post, name="new_post"),
    path('posts/<int:post_id>/edit/', update_post, name="edit_post"),
    path('posts/<int:post_id>/delete/', delete_post, name="remove_post"),
    path('posts/<slug:post_slug>/', get_post_detail, name="post_detail"),
    path('posts/category/<slug:category_slug>/', get_category_posts, name="category_posts"),
    path('posts/tag/<slug:tag_slug>/', get_tag_posts, name="tag_posts"),
    path('', main_page_view, name='main_page'),
]
