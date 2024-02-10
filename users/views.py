from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView
from users.forms import UserRegisterForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import View


User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        # Генерируем токен для верификации
        token = default_token_generator.make_token(user)
        user.verification_token = token
        user.save()

        # Создаем ссылку для верификации почты
        verify_url = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'pk': user.pk, 'token': token})
        )

        # Отправляем письмо для верификации
        subject = 'Подтверждение регистрации'
        message = render_to_string('users/verification_email.html', {'verify_url': verify_url})
        send_mail(subject, message, None, [user.email])

        return super().form_valid(form)

class VerifyEmailView(View):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")

        if user.verification_token == token:
            user.is_verified = True
            user.save()
            messages.success(request, 'Ваш аккаунт успешно активирован. Вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Неверная ссылка для верификации. Пожалуйста, свяжитесь с администратором.')
            return redirect('users:login')


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            # Генерируем новый случайный пароль
            new_password = 'Wereerew1111'
            # Устанавливаем новый пароль для пользователя
            user.set_password(new_password)
            user.save()

            # Отправляем письмо с новым паролем
            subject = 'Сброс пароля'
            message = render_to_string(self.email_template_name, {'new_password': new_password})
            send_mail(subject, message, None, [user.email], html_message=None)

            messages.success(self.request, 'Новый пароль отправлен на ваш email.')
        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь с указанным email не найден.')

        return super().form_valid(form)

class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

