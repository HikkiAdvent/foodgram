from django.urls import path, include
from .views import (
    CustomTokenCreateView, LogoutView, SetPasswordView
)
from djoser.views import UserViewSet

users = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('set_password/', SetPasswordView.as_view(), name='set-password'),
]

auth = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomTokenCreateView.as_view(), name='login'),
]

urlpatterns = [
    path('users/', include(users)),
    path('auth/token/', include(auth))

]
