from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F, Q

from .models import Post, Category, Tag
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status="published").order_by('-created_at')
    paginate_by = 5


class PostSearchView(ListView):
    model = Post
    template_name = "blog/post_search.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_performed'] = any(self.request.GET.keys())

        return context
    
    def get_queryset(self):
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = Post.objects.filter(status="published")

            search_category = self.request.GET.get("search_category")
            search_tag = self.request.GET.get("search_tag")

            query = Q(title__icontains=search_query) | Q(text__icontains=search_query)

            if search_category:
                query |= Q(category__name__icontains=search_query)

            if search_tag:
                query |= Q(tags__name__icontains=search_query)

            return queryset.filter(query).order_by("-created_at")
        
        return Post.objects.none()


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

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        session_key = f'post_{post.id}_viewed'

        if not self.request.session.get(session_key, False):
            Post.objects.filter(id=post.id).update(views=F("views") + 1)

            post.views = post.views + 1

            self.request.session[session_key] = True

        user = self.request.user
        if user.is_authenticated and user != post.author:
            if not post.viewed_users.filter(id=user.id).exists():
                post.viewed_users.add(user)

        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        post = self.object

        context['is_liked'] = False
        context['is_disliked'] = False
        
        if user.is_authenticated:
            context['is_liked'] = post.liked_users.filter(id=user.id).exists()
            context['is_disliked'] = post.disliked_users.filter(id=user.id).exists()

        context['likes_count'] = post.liked_users.count()
        context['dislikes_count'] = post.disliked_users.count()

        return context


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


class PostLikeToggleView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        has_liked = post.liked_users.filter(id=user.id).exists()
        has_disliked = post.disliked_users.filter(id=user.id).exists()

        if has_liked:
            post.liked_users.remove(user)
            has_liked = False
        else:
            post.liked_users.add(user)
            has_liked = True

            if has_disliked:
                post.disliked_users.remove(user)
                has_disliked = False

        likes_count = post.liked_users.count()
        dislikes_count = post.disliked_users.count()

        return JsonResponse({
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'has_liked': has_liked,
            'has_disliked': has_disliked
        })


class PostDislikeToggleView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        has_disliked = post.disliked_users.filter(id=user.id).exists()
        has_liked = post.liked_users.filter(id=user.id).exists()

        if has_disliked:
            post.disliked_users.remove(user)
            has_disliked = False
        else:
            post.disliked_users.add(user)
            has_disliked = True

            if has_liked:
                post.liked_users.remove(user)
                has_liked = False

        dislikes_count = post.disliked_users.count()
        likes_count = post.liked_users.count()

        return JsonResponse({
            'dislikes_count': dislikes_count,
            'likes_count': likes_count,
            'has_disliked': has_disliked,
            'has_liked': has_liked
        })
