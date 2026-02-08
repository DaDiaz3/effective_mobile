from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .jwt import create_access_token
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from .security import hash_password, verify_password


class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        data = s.validated_data

        if User.objects.filter(email=data["email"]).exists():
            return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data.get("last_name", ""),
            patronymic=data.get("patronymic", ""),
            password_hash=hash_password(data["password"]),
            is_active=True,
        )
        return Response({"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        data = s.validated_data

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"detail": "User is inactive"}, status=status.HTTP_403_FORBIDDEN)

        if not verify_password(data["password"], user.password_hash):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token = create_access_token(user.id)
        return Response({"access_token": token, "token_type": "Bearer"})


class MeView(APIView):
    def get(self, request):
        u = getattr(request, "auth_user", None)
        if u is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "id": u.id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "patronymic": u.patronymic,
            "is_active": u.is_active,
        })

    def patch(self, request):
        u = getattr(request, "auth_user", None)
        if u is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        for field in ("first_name", "last_name", "patronymic"):
            if field in request.data:
                setattr(u, field, request.data[field])

        u.save(update_fields=["first_name", "last_name", "patronymic"])

        return Response({
            "id": u.id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "patronymic": u.patronymic,
            "is_active": u.is_active,
        })
    def delete(self, request):
        u = getattr(request, "auth_user", None)
        if u is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        u.is_active = False
        u.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)
