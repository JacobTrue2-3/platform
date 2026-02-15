from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Tag
from .forms import PostForm


def get_post_list(request):
    posts = Post.objects.filter(status="published")

    return render(request, 'blog/post_list.html', context={'posts': posts})


def get_category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status='published')
    
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_posts.html', context)

def get_tag_posts(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blog/tag_posts.html', context)


def get_post_detail(request, post_slug):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, slug=post_slug)

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
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user

            post.save()

            tags = form.cleaned_data.get('tags_input', [])
            
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            return redirect('blog:post_detail', post_slug=post.slug)
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

            tags = form.cleaned_data.get('tags_input', [])
            updated_post.tags.clear()
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                updated_post.tags.add(tag)

            return redirect("blog:post_detail", post_slug=updated_post.slug)
        else:
            return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})

    existing_tags = ", ".join(tag.name for tag in post.tags.all())
    form = PostForm(instance=post, initial={'tags_input': existing_tags})

    return render(request, 'blog/post_form.html', context={"form": form, 'title': title, 'submit_button_text': submit_button_text})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()

        return redirect("blog:post_list")
    
    return render(request, 'blog/confirm_post_delete.html', {'post': post})


def main_page_view(request):
    return render(request, template_name='blog/main_page.html')
