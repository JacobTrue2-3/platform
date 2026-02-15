from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликован'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, editable=False, verbose_name="Слаг")
    category = models.ForeignKey(
        'Category',
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Категория"
    )
    tags = models.ManyToManyField("Tag", related_name='posts', blank=True, verbose_name='Теги')
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # можно указать SET_NULL
    status = models.CharField(choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    viewed_users = models.ManyToManyField(User, blank=True, related_name='viewed_posts', verbose_name="Просмотрено пользователями")
    liked_users = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True,
        verbose_name="Лайки"
    )
    disliked_users = models.ManyToManyField(
        User,
        related_name="disliked_posts",
        blank=True,
        verbose_name="Дизлайки"
    )
    favorites = models.ManyToManyField(
        User,
        related_name="favorite_posts",
        blank=True,
        verbose_name="В избранном у"
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = "Посты"
        db_table = "blog_posts"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))

        super().save(*args, **kwargs)

        # Проверяем, опубликован ли пост, есть ли у этого поста связанная новость и закреплена ли она
        if self.status == "published" and hasattr(self, 'news_item') and self.news_item.pinned:
            # Снимаем закрепление с других новостей
            News.objects.filter(pinned=True).exclude(post_item=self).update(pinned=False)


class News(models.Model):
    post_item = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name='news_item',
        verbose_name="Пост новости"
    )
    is_important = models.BooleanField(verbose_name="Важная новость")
    news_type = models.CharField(
        choices=[
            ('announcement', 'Анонс'),
            ('update', 'Обновление'),
            ('event', 'Событие'),
            ('maintenance', 'Техработы'),
        ],
        verbose_name="Тип новости"
    )
    pinned = models.BooleanField(verbose_name="Закрепленная новость")
    email_notifications_sent = models.BooleanField(default=False, verbose_name="Email-уведомления отправлены")
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = "Новости"
        db_table = "blog_news"

    def __str__(self):
        return f"{self.post_item.title}"

    def save(self, *args, **kwargs):
        # Если новость закрепляется, снимаем закрепление с других новостей
        if self.pinned and self.post_item.status == "published":
            News.objects.filter(pinned=True).exclude(id=self.id).update(pinned=False)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, editable=False, verbose_name="Слаг")

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'category_slug': self.slug})
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        db_table = "blog_categories"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, editable=False, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.name}'
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', args=[self.slug])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"
        db_table = "blog_tags"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent:
            parent_text = self.parent.text[:20] + '...' if len(self.parent.text) > 20 else self.parent.text
            reply_text = self.text[:20] + '...' if len(self.text) > 20 else self.text
            return f'Ответ польз. {self.author} на комментарий польз. {self.parent.author}: комм. "{parent_text}", отв. "{reply_text}"'
        
        return f'Комментарий от {self.author} к "{self.post}": {self.text if len(self.text) < 20 else self.text[:20] + '...'}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"
        db_table = "blog_comments"
