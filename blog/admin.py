from django.contrib import admin
from django.utils import timezone
from .models import Post, News, Category, Tag, Comment

# Actions для массовой публикации/снятия с публикации
def make_published(modeladmin, request, queryset):
    # Публикуем только те посты, которые еще не опубликованы
    updated = queryset.filter(status='draft').update(status='published')
    
    if updated == 1:
        message = "1 пост был опубликован"
    elif updated > 1:
        message = f"{updated} постов были опубликованы"
    else:
        message = "Не выбрано постов для публикации (все уже опубликованы)"
    
    modeladmin.message_user(request, message)
make_published.short_description = "Опубликовать выбранные посты"

def make_draft(modeladmin, request, queryset):
    # Переводим в черновик только опубликованные посты
    updated = queryset.filter(status='published').update(status='draft')
    
    if updated == 1:
        message = "1 пост переведен в черновик"
    elif updated > 1:
        message = f"{updated} постов переведены в черновик"
    else:
        message = "Не выбрано постов для перевода в черновик (все уже в черновиках)"
    
    modeladmin.message_user(request, message)
make_draft.short_description = "Перевести в черновик"

# Кастомный админ класс для Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'author', 'created_at', 'views']
    list_filter = ['status', 'category', 'author', 'created_at']
    search_fields = ['title', 'text']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at']
    actions = [make_published, make_draft]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'text', 'image', 'category', 'tags')
        }),
        ('Статус и автор', {
            'fields': ('status', 'author')
        }),
        ('Статистика', {
            'fields': ('views', 'created_at', 'updated_at', 'slug'),
            'classes': ('collapse',)
        }),
        ('Лайки и избранное', {
            'fields': ('liked_users', 'disliked_users', 'favorites', 'viewed_users'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['tags', 'liked_users', 'disliked_users', 'favorites', 'viewed_users']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Если это новый пост
            obj.author = request.user  # Автоматически устанавливаем автора
        super().save_model(request, obj, form, change)

# Регистрация остальных моделей
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('name',)}  # Но у вас slug автоматически генерируется в save

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    readonly_fields = ['slug']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'created_at', 'short_text']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'post__title']
    readonly_fields = ['created_at']
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст комментария'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['post_title', 'is_important', 'news_type', 'pinned', 'email_notifications_sent', 'post_status']
    list_filter = ['is_important', 'news_type', 'pinned', 'email_notifications_sent', 'post_item__status']
    search_fields = ['post_item__title']
    raw_id_fields = ['post_item']  # Удобно для выбора поста
    
    def post_title(self, obj):
        return obj.post_item.title
    post_title.short_description = 'Заголовок поста'
    
    def post_status(self, obj):
        return obj.post_item.status
    post_status.short_description = 'Статус поста'
    post_status.admin_order_field = 'post_item__status'
    
    actions = ['mark_as_important', 'unmark_as_important', 'mark_pinned']
    
    def mark_as_important(self, request, queryset):
        updated = queryset.update(is_important=True)
        self.message_user(request, f"{updated} новостей отмечены как важные")
    mark_as_important.short_description = "Отметить как важные"
    
    def unmark_as_important(self, request, queryset):
        updated = queryset.update(is_important=False)
        self.message_user(request, f"{updated} новостей сняты с отметки 'важные'")
    unmark_as_important.short_description = "Снять отметку 'важные'"
    
    def mark_pinned(self, request, queryset):
        # Снимаем закрепление со всех других новостей
        News.objects.filter(pinned=True).update(pinned=False)
        # Закрепляем выбранные
        updated = queryset.update(pinned=True)
        self.message_user(request, f"{updated} новостей закреплены")
    mark_pinned.short_description = "Закрепить выбранные новости"