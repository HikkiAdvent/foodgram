from django.contrib import admin
from django.contrib.auth import get_user_model

from users import models

User = get_user_model()


class FollowerInline(admin.TabularInline):
    model = models.Subscription
    fk_name = 'user'
    extra = 0


class FavoriteInline(admin.TabularInline):
    model = models.Favorite
    extra = 0


class ShoppingListInline(admin.TabularInline):
    model = models.ShoppingCart
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    inlines = (FollowerInline, FavoriteInline, ShoppingListInline)
    search_fields = ('username', 'email')
