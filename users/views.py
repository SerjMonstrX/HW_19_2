from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import get_user_model, login
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


class RegisterView(CreateView):
   model = User
   form_class = UserRegisterForm
   success_url = reverse_lazy('users:login')
   template_name = 'users/register.html'

   def form_valid(self, form):
      user = form.save(commit=False)
      user.is_verified = False
      user.save()

      # Создаем токен для подтверждения почты
      token = default_token_generator.make_token(user)
      uidb64 = urlsafe_base64_encode(user.pk.to_bytes(4, 'big'))  # преобразуем PK пользователя в bytes

      # Создаем ссылку для верификации почты
      verify_url = self.request.build_absolute_uri(
         reverse_lazy('users:verify_email', kwargs={'uidb64': uidb64, 'token': token})
      )

      # Формируем сообщение для отправки
      subject = 'Подтверждение регистрации'
      message = render_to_string(
         'users/verification_email.html',  # Шаблон письма
         {'verify_url': verify_url}  # Контекст для шаблона
      )
      recipient = user.email

      # Отправляем письмо
      send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

      # После успешной регистрации, автоматически авторизуем пользователя
      login(self.request, user)
      return redirect(self.success_url)


class VerifyEmailView(View):

   def get(self, request, uidb64, token):
      try:
         # Декодируем uidb64 для получения идентификатора пользователя
         uid = urlsafe_base64_decode(uidb64)
         user = User.objects.get(pk=uid)
      except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
         raise Http404  # Отправляем 404 ошибку если uidb64 некорректен или пользователь не найден

      if user is not None and default_token_generator.check_token(user, token):
         # Если пользователь существует и токен верен, активируем аккаунт пользователя
         user.is_verified = True
         user.save()
         messages.success(request, 'Ваш аккаунт успешно активирован. Вы можете войти.')
         login(request, user)
         return redirect('users:login')
      else:
         # Если пользователь не найден или токен неверный, выводим сообщение об ошибке
         messages.error(request, 'Неверная ссылка для верификации. Пожалуйста, свяжитесь с администратором.')
         return redirect(reverse_lazy('users:login'))