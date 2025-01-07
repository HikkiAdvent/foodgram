from django.urls import path, include
from djoser.views import UserViewSet

users = [
    # path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', UserViewSet.as_view({'get': 'list'}), name='list'),
    path('', UserViewSet.as_view({'post': 'create'}), name='register'),
]


urlpatterns = [
    # path('', include(auth)),
    path('users/', include(users))

]
