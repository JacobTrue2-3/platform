from django.contrib.auth import get_user_model
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.auth.decorators import login_required
# from django.conf import settings

from config.settings import LOGIN_REDIRECT_URL, DEFAULT_FROM_EMAIL, FIREBASE_API_KEY
from blog.models import Post
from .forms import CustomAuthenticationForm, CustomUserCreationForm

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/pages/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        # Сохраняем пользователя как неактивного
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Отправляем письмо активации
        self.send_activation_email(user)

        messages.success(
            self.request, 
            'Регистрация прошла успешно! Проверьте почту для активации аккаунта.'
        )
        return redirect('users:login')
        # Используем явный redirect, чтобы избежать повторного form.save() в super().form_valid(form)
        # второй save() менял пользователя и делал токен недействительным

    def send_activation_email(self, user):
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        
        activation_url = self.request.build_absolute_uri(
            reverse_lazy('users:activate_account', kwargs={'uidb64': uidb64, 'token': token})
        )
        
        site_name = get_current_site(self.request).name

        subject = render_to_string('users/emails/subjects/activate_account.txt', {
            'site_name': site_name,
        })
        message = render_to_string('users/emails/activate_account.txt', {
            'site_name': site_name,
            'activation_url': activation_url
        })
        html_message = render_to_string('users/emails/activate_account.html', {
            'site_name': site_name,
            'activation_url': activation_url
        })

        send_mail(
            subject=subject,
            message=message,  # Текстовая версия
            html_message=html_message,  # HTML версия
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Аккаунт успешно активирован! Теперь вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Ссылка активации недействительна или устарела.')
            return redirect('users:register')


class CustomLoginView(LoginView):
    template_name = 'users/pages/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', LOGIN_REDIRECT_URL)
        if next_url == LOGIN_REDIRECT_URL:
            return reverse_lazy(next_url, kwargs={'user_username': self.request.user.username})
        return next_url
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Ошибка входа!')

        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blog:post_list')


@require_POST
@login_required
def set_phone_number(request):
    try:
        # Преобразуем строку в объект PhoneNumber
        parsed_phone_number = PhoneNumber.from_string(request.POST.get('phone_number'), region='RU')
        if parsed_phone_number.is_valid():
            # Проверяем, не пытается ли пользователь установить тот же номер телефона
            if request.user.phone_number == parsed_phone_number:
                messages.info(request, 'Этот номер телефона уже привязан к вашему аккаунту')
                return redirect('users:settings')
            
            # Проверяем, не подтвержден ли этот номер телефона у другого пользователя
            user_verified_this_number = User.objects.filter(
                phone_number=parsed_phone_number, 
                phone_number_verified=True
            )
            
            if user_verified_this_number.exists():
                messages.warning(request, 'Этот номер телефона уже используется другим пользователем')
                return redirect('users:settings')

            # Определяем сообщение в зависимости от того, был ли номер телефона до этого
            if request.user.phone_number:
                message = 'Номер телефона успешно изменён'
            else:
                message = 'Номер телефона успешно добавлен'

            request.user.phone_number = parsed_phone_number
            request.user.phone_number_verified = False  # Сбрасываем статус верификации
            request.user.save()
            messages.success(request, message)
        else:
            messages.warning(request, 'Некорректный формат номера телефона')
    except Exception as e:
        messages.warning(request, 'Указанное вами, похоже, не является номером телефона.')
    
    return redirect('users:settings')


@require_POST
@login_required
def mark_phone_number_as_verified(request):
    # Клиент уже проверил код
    # Обновляем статус верификации номера телефона
    request.user.phone_number_verified = True
    request.user.save()

    # Удаляем этот номер телефона у других пользователей
    users_not_verified_this_number = User.objects.filter(
        phone_number=request.user.phone_number
    ).exclude(id=request.user.id)

    if users_not_verified_this_number.exists():
        for user in users_not_verified_this_number:
            user.phone_number = None
            user.save()
    
    return JsonResponse({'success': True})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/pages/password_change.html'
    success_url = reverse_lazy('users:password_change_done')
    
    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)


class PasswordChangeDoneView(TemplateView):
    template_name = 'users/pages/password_change_done.html'


class ProfilePasswordResetView(PasswordResetView):
    template_name="users/pages/password_reset_profile.html"
    email_template_name='users/emails/password_reset.txt',
    html_email_template_name='users/emails/password_reset.html',
    subject_template_name='users/emails/subjects/password_reset.txt'
    success_url=reverse_lazy("users:profile_password_reset_instructions_sent")

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['email'] = request.user.email

        messages.success(request, f'Письмо отправлено на {request.user.email}')

        return super().post(request, *args, **kwargs)


@require_POST
def toggle_theme(request):
    if request.user.is_authenticated:
        # Для авторизованных — меняем в базе
        new_theme = 'light' if request.user.selected_theme == 'dark' else 'dark'
        request.user.selected_theme = new_theme
        request.user.save(update_fields=["selected_theme"])
    else:
        # Для неавторизованных — меняем в сессии
        current_theme = request.session.get('theme', 'dark')
        new_theme = 'light' if current_theme == 'dark' else 'dark'
        request.session['theme'] = new_theme
    
    return JsonResponse({'new_theme': new_theme})


class ProfileView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'users/pages/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'user_username'
    context_object_name = 'user' # Теперь обязательно
    paginate_by = 5

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(
            author=self.object
        ).order_by('-created_at')

        # Контекст теперь включает paginator, page_obj, is_paginated
        context = super().get_context_data(object_list=posts, **kwargs)
        
        context['posts'] = context['object_list']
        
        del context['object_list']

        return context


class FavoritePostsView(ListView):
    model = Post
    template_name = 'users/pages/favorite_posts.html'
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        return self.request.user.favorite_posts.all()


class SettingsView(TemplateView):
    """Страница настроек профиля"""
    template_name = 'users/pages/settings.html'
    extra_context = {
        'FIREBASE_API_KEY': FIREBASE_API_KEY,
    }
