from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

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
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    inlines = (FollowerInline, FavoriteInline, ShoppingListInline)
    search_fields = ('username', 'email')

    def get_inline_instances(self, request, obj=None):
        """Показывает инлайны только при редактировании."""

        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('recipe',)


@admin.register(models.ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('recipe',)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if obj.user == obj.author:
            self.message_user(
                request,
                "Нельзя подписаться на самого себя!",
                level="error"
            )
            return
        super().save_model(request, obj, form, change)
