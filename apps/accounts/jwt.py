import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
print("JWT SETTINGS:", settings.JWT_SECRET, settings.JWT_ALG)

def create_access_token(user_id: int) -> str:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(minutes=int(getattr(settings, "JWT_TTL_MIN", 60)))

    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "type": "access",
    }
    print("ENCODE USING:", settings.JWT_SECRET, settings.JWT_ALG)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_access_token(token: str):
    try:
        print("DECODE USING:", settings.JWT_SECRET, settings.JWT_ALG)
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
            options={"verify_signature": True, "verify_exp": True},
        )
    except Exception as e:
        print("JWT DECODE ERROR:", repr(e))
        return None

    user_id = payload.get("sub")
    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None