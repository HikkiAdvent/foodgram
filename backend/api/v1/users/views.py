from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenCreateView(APIView):
    """Кастомный View для создания токена."""
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token_data = serializer.save()
        return Response(token_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Кастомный View для выхода пользователя."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"detail": "Authorization header is required."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token = auth_header.split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(APIView):
    """Кастомный View для обновления пароля."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response({"detail": _("Both current and new passwords are required.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"detail": _("Current password is incorrect.")},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
