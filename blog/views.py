from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm


def get_post_list(request):
    posts = Post.objects.all()

    return render(request, 'blog/post_list.html', context={'posts': posts})


def get_post_detail(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)

    context = {'post': post}

    return render(request, 'blog/post_detail.html', context)


@login_required
def create_post(request):
    title = "Создать пост"
    submit_button_text = 'Создать'

    if request.method == "GET":
        form = PostForm()

        return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})
    
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user

            post.save()

            return redirect('blog:post_detail', post_id=post.id)
        else:
            return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})


def update_post(request, post_id):
    title = "Редактировать пост"
    submit_button_text = 'Обновить'

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            updated_post = form.save()

            return redirect("blog:post_detail", post_id=updated_post.id)
        else:
            return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})

    form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()

        return redirect("blog:post_list")
    
    return render(request, 'blog/confirm_post_delete.html', {'post': post})


def main_page_view(request):
    return render(request, template_name='blog/main_page.html')
