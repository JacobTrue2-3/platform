from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy

from config.settings import LOGIN_REDIRECT_URL
from blog.models import Post

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next', LOGIN_REDIRECT_URL) # '/posts/add/'
            if next_url == LOGIN_REDIRECT_URL:
                return redirect(next_url, request.user.username)
            else:
                return redirect(next_url)
        else:
            return render(request, 'users/login.html', {'form': form})


    form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


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
