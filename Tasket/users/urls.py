from django.urls import path
from .views import UserApiView


app_name = 'users'

urlpatterns = [
    path('users', UserApiView.as_view()),
    path('users/<int:pk>', UserApiView.as_view())
]
