import secrets

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from users.services.account_confirmed import account_confirmed


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.is_active = False
            self.object.token = secrets.token_urlsafe(18)[:15]
            self.object.save()
            account_confirmed(self.object)
            self.user_token = self.object.token
        return super().form_valid(form)

    def get_success_url(self):
        new_url = super().get_success_url()
        token = self.object.token
        return str(new_url) + str(token)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, token):
    if request.method == 'POST':
        obj = get_object_or_404(User, token=token)
        obj.is_active = True
        obj.save()
    return render(request, 'users/verify_email.html')


def activate_user(request, token):
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()
        return redirect('users:login')
    return render(request, 'users/user_not_found.html')


class PasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


@login_required
def password_reset_done(request):
    pass_ch = secrets.token_urlsafe(18)[:9]
    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш новый пароль {pass_ch}',
        recipient_list=[request.user.email]
    )
    user = request.user
    user.set_password(pass_ch)
    user.save()
    return redirect(reverse('users:password_reset_done'))


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Override method to include only active users."""
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

