from django.contrib.auth.models import AnonymousUser

from apps.accounts.jwt import decode_access_token
from apps.accounts.models import User


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(">>> AUTH MIDDLEWARE HIT:", request.path)
        request.user = AnonymousUser()
        request.auth_user = None

        auth = request.headers.get("Authorization")
        print("AUTH HEADER:", auth)

        if auth:
            parts = auth.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
                user_id = decode_access_token(token)
                print("DECODED USER_ID:", user_id)

                if user_id:
                    try:
                        user = User.objects.get(id=user_id, is_active=True)
                        print("USER FOUND:", user.email)

                        request.user = user
                        request.auth_user = user
                        request._cached_user = user

                    except User.DoesNotExist:
                        print("USER NOT FOUND OR INACTIVE:", user_id)

        return self.get_response(request)
