from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
  THEME_CHOICES = [
    ("light", "Светлая"),
    ("dark", "Тёмная")
  ]

  email = models.EmailField(unique=True, null=True, blank=True)
  avatar = models.ImageField(upload_to="user_avatars/", null=True, blank=True)
  selected_theme = models.CharField(choices=THEME_CHOICES, default="dark")
  subscribed_to_important_news = models.BooleanField(
    default=False,
    verbose_name="Подписан на важные новости"
  )

  class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = "Пользователи"
