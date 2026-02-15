from django.shortcuts import render, get_object_or_404
from .models import Post


def get_post_list(request):
    posts = Post.objects.all()

    return render(request, 'blog/post_list.html', context={'posts': posts})


def get_post_detail(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)

    context = {'post': post}

    return render(request, 'blog/post_detail.html', context)
