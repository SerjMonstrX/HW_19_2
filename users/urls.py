from django.urls import path
from users.views import RegisterView, VerifyEmailView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/<int:pk>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
]

