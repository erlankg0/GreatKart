from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView  # Reset password.
from django.urls import path

from accounts.views import SignInView, SignOutView, SignUpView

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),  # Sign In.
    path('sign_out/', SignOutView.as_view(), name='sign_out'),  # Sign Out.
    path('sign_up/', SignUpView.as_view(), name='sign_up'),  # Sign Up.
    # change password. ------------------------------------------ #  смена пароля.
    path('password/change/', PasswordChangeView.as_view(
        template_name='accounts/change_password.html'
    ), name='password_change'),  # Change password.
    path('password/change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html'
    ), name='password_reset'),  # Done password reset.
    # reset password. ------------------------------------------- #  сброс пароля.
    path('password/reset/', PasswordResetView.as_view(
        template_name='accounts/reset_password.html'
    ), name='password_reset'),  # Reset password.
    path('password/reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/done_password_reset.html'
    ), name='password_reset_done'),  # Done password reset.
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/confirm_password_reset.html'
    ), name='password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/confim_password_reset_done.html'
    ), name='password_reset_complete'),
    # Done password reset.

]
