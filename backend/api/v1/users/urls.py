from django.urls import path, include
from .views import (
    CustomTokenCreateView, CustomTokenDestroyView, SetPasswordView
)
from djoser.views import UserViewSet

users = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('set_password/', SetPasswordView.as_view(), name='set-password'),
]

auth = [
    path('logout/', CustomTokenDestroyView.as_view(), name='token_logout'),
    path('login/', CustomTokenCreateView.as_view(), name='login'),
]

urlpatterns = [
    path('users/', include(users)),
    path('auth/token/', include(auth))

]
