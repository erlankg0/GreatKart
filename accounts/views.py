from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView, \
    PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import AccountAuthForm, AccountCreateForm
from accounts.forms import AccountChangePassword


# Вход, Выход, Регистрация.
# Sign In, Sign Out, Sign Up.
class SignInView(LoginView):
    """Sign In View"""
    template_name = 'accounts/singin.html'
    form_class = AccountAuthForm
    success_url = '/'

    def get_success_url(self):
        return self.success_url


class SignOutView(LoginRequiredMixin, LogoutView):
    """Sign Out View"""
    template_name = 'store/index.html'


class SignUpView(CreateView):
    """Sign Up View"""
    template_name = 'accounts/singup.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('home')


# Change password.
class ChangePasswordView(PasswordChangeView):
    """Change Password View"""
    template_name = 'accounts/change_password.html'
    form_class = AccountChangePassword
    success_url = reverse_lazy('home')


# Change password done.
class ChangePasswordDoneView(PasswordResetDoneView):
    """Change Password Done View"""
    template_name = 'accounts/change_password_done.html'
    success_url = reverse_lazy('home')


# Reset password.
class ResetPasswordView(PasswordResetView):
    """Reset Password View"""
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('done_password_reset')
    email_template_name = 'accounts/done_password_reset.html'


class DonePasswordResetView(PasswordResetDoneView):
    """Done Password Reset View"""
    template_name = 'accounts/done_password_reset.html'  # Done password reset.
