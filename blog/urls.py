from django.urls import path

from .views import get_post_list, get_post_detail, create_post

urlpatterns = [
    path("posts/", get_post_list, name="post_list"),
    path('posts/<int:post_id>/', get_post_detail, name="post_detail"),
    path('posts/add/', create_post, name="new_post")
]
