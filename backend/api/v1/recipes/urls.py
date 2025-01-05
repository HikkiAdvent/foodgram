from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.recipes import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('tags', views.TagViewSet, basename='tags')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls))
]
