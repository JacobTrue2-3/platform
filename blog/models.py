from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # можно указать SET_NULL

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = "Посты"
        db_table = "blog_posts"

    def __str__(self):
        return self.title

# null, default
