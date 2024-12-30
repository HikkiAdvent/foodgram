from django.urls import path, include

auth = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]


urlpatterns = [
    path('auth/', include(auth)),
]
