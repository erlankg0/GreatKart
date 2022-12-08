from django.urls import path
from accounts.views import SignInView, SignOutView, SignUpView

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('sign_out/', SignOutView.as_view(), name='sign_out'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
]
