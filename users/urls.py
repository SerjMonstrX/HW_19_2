from django.urls import path
from users.views import RegisterView, VerifyEmailView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('verify_email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
