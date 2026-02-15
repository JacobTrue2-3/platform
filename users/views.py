from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404

from config.settings import LOGIN_REDIRECT_URL
from blog.models import Post
from .forms import CustomAuthenticationForm

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/pages/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):
    template_name = 'users/pages/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', LOGIN_REDIRECT_URL)
        if next_url == LOGIN_REDIRECT_URL:
            return reverse_lazy(next_url, kwargs={'user_username': self.request.user.username})
        return next_url
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Ошибка входа!')

        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blog:post_list')


class ProfileView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'users/pages/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'user_username'
    # context_object_name = 'user' Необязательно
    paginate_by = 5

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(
            author=self.object
        ).order_by('-created_at')

        # Контекст теперь включает paginator, page_obj, is_paginated
        context = super().get_context_data(object_list=posts, **kwargs)
        
        context['posts'] = context['object_list']
        
        del context['object_list']

        return context


class FavoritePostsView(ListView):
    model = Post
    template_name = 'users/pages/favorite_posts.html'
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        return self.request.user.favorite_posts.all()
