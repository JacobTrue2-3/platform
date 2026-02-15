from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, get_user_model
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from config.settings import LOGIN_REDIRECT_URL
from blog.models import Post

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', LOGIN_REDIRECT_URL)
        if next_url == LOGIN_REDIRECT_URL:
            return reverse_lazy(next_url, kwargs={'user_username': self.request.user.username})
        return next_url


def logout_view(request):
    logout(request)
    return redirect("blog:post_list")


def profile_view(request, user_username):
    user = get_object_or_404(User, username=user_username)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,
        'posts': posts
    }

    return render(request, 'users/profile.html', context)
