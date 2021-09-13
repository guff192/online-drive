from django.urls import path, include
import django.contrib.auth.urls as auth_urls

urlpatterns = [
    path('', include(auth_urls)),
]
