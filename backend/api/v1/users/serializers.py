from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')


class CustomTokenCreateSerializer(serializers.Serializer):
    """Сериализатор для получения токена по email и паролю."""
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError(_("Unable to log in with provided credentials."), code='authorization')
        else:
            raise serializers.ValidationError(_("Must include 'email' and 'password'."), code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token = RefreshToken.for_user(user)
        return {'auth_token': str(token.access_token)}


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор для отображения данных пользователя."""

    is_subscribed = serializers.SerializerMethodField()  # Для вычисления подписки
    avatar = serializers.ImageField(source='avatar', required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        """Проверка, подписан ли текущий пользователь на данного пользователя."""
        user = self.context['request'].user
        if user.is_authenticated:
            return user.subscriptions.filter(id=obj.id).exists()
        return False
