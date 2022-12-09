from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
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


class SignOutView(LogoutView):
    """Sign Out View"""
    template_name = 'store/index.html'


class SignUpView(CreateView):
    """Sign Up View"""
    template_name = 'accounts/singup.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('home')


# Поменять пароль, Забыл пароль
# Change password, Forgot password
class ChangePasswordView(PasswordChangeView):
    form_class = AccountChangePassword
    template_name = 'accounts/forgot.html'
    success_url = reverse_lazy('password_change_done')
