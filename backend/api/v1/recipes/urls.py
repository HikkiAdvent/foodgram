from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.recipes.views import RecipeViewSet

router = DefaultRouter()
router.register('recipe', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls))
]
