from django.core.mail import send_mail
from django.conf import settings

subject = 'Тестовое письмо'
message = 'Привет! Это тестовое письмо, отправленное из Django.'
from_email = settings.EMAIL_HOST_USER  # Используем ваш адрес электронной почты для отправки
to_email = ['cosmusbz@mail.ru']  # Замените на ваш адрес электронной почты

send_mail(subject, message, from_email, to_email)