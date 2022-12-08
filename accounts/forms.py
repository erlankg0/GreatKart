import unicodedata
from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from accounts.models import Account

# Получения модели учетной записи
UserModel = get_user_model()


class EmailField(forms.CharField):
    """Создаем класс как UserNameField """

    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "email",
        }


# Менеджер Входа (Manager Authentication)
class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """

    email = EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields["email"].max_length = email_max_length
        self.fields["email"].widget.attrs["maxlength"] = email_max_length
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.email_field.verbose_name},
        )


# Creation

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Account
        fields = ("email",)
        field_classes = {"email": EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Form Authentication (Форма авторизации)
class AccountAuthForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'password',)


# Form Create User
class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'phone', 'username', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'type': 'email',
                    'placeholder': 'Э-почта',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя пользователя',
                    'type': 'text'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Номер телефона',
                    'type': 'tel'
                }
            ),
        }


# Form Change Password
class AccountChangePassword(PasswordChangeForm):
    pass
