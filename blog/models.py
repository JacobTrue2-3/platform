from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, editable=False, verbose_name="Слаг")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # можно указать SET_NULL

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = "Посты"
        db_table = "blog_posts"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))

        super().save(*args, **kwargs)

# default
