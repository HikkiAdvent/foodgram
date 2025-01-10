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


class CustomTokenDestroyView(APIView):
    """Удаление JWT токена."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # JWT не удаляется с сервера, просто возвращаем статус 204
        return Response(status=status.HTTP_204_NO_CONTENT)


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
