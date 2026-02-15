from django import forms

class PostForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        label='Заголовок поста:',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'заголовок (максимальная длина 200 символов)'
        }) # Можно передавать другие атрибуты, например, 'class': 'title-input'
    )

    text = forms.CharField(
        label="Текст поста:",
        widget=forms.Textarea(attrs={
            'rows': 3
        })
    )

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) < 5:
            raise forms.ValidationError("Заголовок не должен быть короче 5 символов")
        
        return title
