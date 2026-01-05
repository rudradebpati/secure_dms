# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.db import transaction
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )
