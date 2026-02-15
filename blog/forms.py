from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую'
        }),
        label="Теги"
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "заголовок (максимальная длина 200 символов)"
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Заголовок поста:',
            'category': 'Категория:',
            'text': 'Текст поста:',
            'image': 'Картинка поста'
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) < 5:
            raise forms.ValidationError("Заголовок не должен быть короче 5 символов")
        
        return title

    def clean_tags_input(self):
        """
        Разбиваем строку на список тегов:
        - удаляем лишние пробелы вокруг
        - приводим к нижнему регистру
        """
        tags_str = self.cleaned_data.get('tags_input', '')
        tags = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
        return tags
