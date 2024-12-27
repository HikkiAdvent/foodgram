from django.contrib import admin

from users.models.users import User
from users.models.followers import Follower
from users.models.favorites import Favorite
from users.models.shopping_lists import ShoppingList


class FollowerInline(admin.TabularInline):
    model = Follower
    fk_name = 'user'
    extra = 0


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0


class ShoppingListInline(admin.TabularInline):
    model = ShoppingList
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
    )
    inlines = (FollowerInline, FavoriteInline, ShoppingListInline)
