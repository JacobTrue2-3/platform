from django.urls import path
from .views import (
    MainPageView, PostListView, PostSearchView, CategoryPostsView, TagPostsView,
    PostDetailView, CreatePostView, PostUpdateView, PostDeleteView,
    PostLikeToggleView, PostDislikeToggleView
)

app_name = 'blog'

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/search/", PostSearchView.as_view(), name="post_search"),
    path('posts/add/', CreatePostView.as_view(), name="new_post"),
    path('posts/<int:post_id>/edit/', PostUpdateView.as_view(), name="edit_post"),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name="remove_post"),
    path('posts/<slug:post_slug>/', PostDetailView.as_view(), name="post_detail"),
    path('posts/category/<slug:category_slug>/', CategoryPostsView.as_view(), name="category_posts"),
    path('posts/tag/<slug:tag_slug>/', TagPostsView.as_view(), name="tag_posts"),
    path('posts/<int:post_id>/like/', PostLikeToggleView.as_view(), name="post_like"),
    path('posts/<int:post_id>/dislike/', PostDislikeToggleView.as_view(), name="post_dislike"),
    path('', MainPageView.as_view(), name='main_page'),
]
