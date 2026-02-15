from django.urls import path

from .views import get_post_list

urlpatterns = [
    path("posts/", get_post_list)
]
