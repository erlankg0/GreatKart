from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from accounts.views import SignInView, SignOutView, SignUpView

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),  # Sign In.
    path('sign_out/', SignOutView.as_view(), name='sign_out'),  # Sign Out.
    path('sign_up/', SignUpView.as_view(), name='sign_up'),  # Sign Up.
    path('password/change/', PasswordChangeView.as_view(
        template_name='accounts/change_password.html'
    ), name='password_change'),  # Change password.
    path('password/change/done/', PasswordResetDoneView.as_view(), name='password_reset'),  # Done password reset.
    path('password/reset/', PasswordResetView.as_view(
        template_name='accounts/reset_password.html',
    ), name='reset_password'),  # Reset password.
    path('password/done/', PasswordResetDoneView.as_view(
        template_name='accounts/done_password_reset.html',
    ), name='done_password_reset'),  # Done password reset.
    path('password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/confirm_password_reset.html',
    ), name='confirm_password_reset'),  # Confirm password reset.
    path('password/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/complete_password_reset.html',
    ), name='complete_password_reset'),  # Complete password reset.

]
