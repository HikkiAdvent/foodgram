from django.urls import path, include

urlpatterns = [
    path('', include('api.v1.urls'))
    # Убрал версию для соответствия документации
]
