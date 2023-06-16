from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, activate_user, verify_email, PasswordResetView, CustomPasswordResetForm, password_reset_done

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:token>/', verify_email, name='verify_email'),
    path('activate/<str:token>/', activate_user, name='activate'),
    path('password_reset/', PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),
    path('password_reset_done/', password_reset_done, name='password_reset_done'),
]