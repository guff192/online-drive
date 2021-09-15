from django.urls import path, include
import django.contrib.auth.urls as auth_urls

from accounts.views import SignUpView, profile, change_profile, change_avatar

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', profile, name='profile'),
    path('change_profile/', change_profile, name='change_profile'),
    path('change_avatar/', change_avatar, name='change_avatar'),
    path('', include(auth_urls)),
]
