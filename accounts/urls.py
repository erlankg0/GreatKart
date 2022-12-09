from django.urls import path
from accounts.views import SignInView, SignOutView, SignUpView
from accounts.views import ChangePasswordView

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('sign_out/', SignOutView.as_view(), name='sign_out'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
]
