from django.urls import path
from .views import (
    main_page_view, PostListView, CategoryPostsView, TagPostsView,
    PostDetailView, create_post, update_post,
    delete_post
)

app_name = 'blog'

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path('posts/add/', create_post, name="new_post"),
    path('posts/<int:post_id>/edit/', update_post, name="edit_post"),
    path('posts/<int:post_id>/delete/', delete_post, name="remove_post"),
    path('posts/<slug:post_slug>/', PostDetailView.as_view(), name="post_detail"),
    path('posts/category/<slug:category_slug>/', CategoryPostsView.as_view(), name="category_posts"),
    path('posts/tag/<slug:tag_slug>/', TagPostsView.as_view(), name="tag_posts"),
    path('', main_page_view, name='main_page'),
]
