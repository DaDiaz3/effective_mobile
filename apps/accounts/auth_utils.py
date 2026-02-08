from rest_framework.response import Response
from rest_framework import status


def require_user(request):
    if getattr(request, "user", None) is None:
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)
    return None
