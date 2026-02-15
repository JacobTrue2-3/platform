from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Post, Category, Tag
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status="published").order_by('-created_at')
    paginate_by = 5


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self.category
        
        return context


class TagPostsView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=self.tag, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag'] = self.tag

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # context_object_name = 'post' Необязательно
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug' # Необязательно


class CreatePostView(LoginRequiredMixin, CreateView):
    # model = Post Необязательно
    form_class = PostForm
    template_name = 'blog/post_form.html'
    extra_context = {
        'title': "Создать пост",
        'submit_button_text': "Создать"
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        tags = form.cleaned_data.get('tags_input', [])
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return redirect('blog:post_detail', post_slug=post.slug)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    pk_url_kwarg = 'post_id'  # потому что в url <int:post_id>, а не <int:id>

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = "Редактировать пост"
        context['submit_button_text'] = "Обновить"
        context['form'].fields['tags_input'].initial = ", ".join(tag.name for tag in self.object.tags.all())
        
        return context

    def form_valid(self, form):
        updated_post = form.save()

        tags = form.cleaned_data.get('tags_input', [])
        updated_post.tags.clear()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            updated_post.tags.add(tag)

        return redirect('blog:post_detail', post_slug=self.object.slug)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/confirm_post_delete.html'
    # context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')


class MainPageView(TemplateView):
    template_name = 'blog/main_page.html'
