from django.urls import path
# from django.urls import reverse_lazy
# from django.contrib.auth.views import PasswordChangeView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    # path('password-change/', PasswordChangeView.as_view(
    #     template_name='users/pages/password_change.html',
    #     success_url=reverse_lazy('users:password_change_done')
    # ), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),

    path("favorite-posts/", views.FavoritePostsView.as_view(), name="favorite_posts"),
    path("<str:user_username>/", views.ProfileView.as_view(), name='profile'),
]
