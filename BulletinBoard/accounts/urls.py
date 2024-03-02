from django.urls import path

from .views import ProfileUser

urlpatterns = [
    path('profile/', ProfileUser.as_view(), name='profile'),
]