from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/load-more/", views.LoadMorePostsView.as_view(), name="load_more_posts"),
    path("posts/search/", views.PostSearchView.as_view(), name="post_search"),
    path('posts/add/', views.CreatePostView.as_view(), name="new_post"),
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name="edit_post"),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name="remove_post"),
    path('posts/<slug:post_slug>/', views.PostDetailView.as_view(), name="post_detail"),
    path('posts/category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name="category_posts"),
    path('posts/tag/<slug:tag_slug>/', views.TagPostsView.as_view(), name="tag_posts"),
    path('posts/<int:post_id>/like/', views.PostLikeToggleView.as_view(), name="post_like"),
    path('posts/<int:post_id>/dislike/', views.PostDislikeToggleView.as_view(), name="post_dislike"),
    path('posts/<int:post_id>/toggle-favorite/', views.PostFavoriteToggleView.as_view(), name="post_favorite_toggle"),
    path("posts/<int:post_id>/comments/add/", views.AddCommentView.as_view(), name="add_comment"),
    path('posts/<int:post_id>/comments/load-more/', views.LoadMoreCommentsView.as_view(), name="load_more_comments"),
    path('', views.MainPageView.as_view(), name='main_page'),
]
