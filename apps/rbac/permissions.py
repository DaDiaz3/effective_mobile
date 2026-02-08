from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from apps.rbac.models import BusinessElement, AccessRule, UserRole

METHOD_TO_ACTION = {
    "GET": "read",
    "POST": "create",
    "PUT": "update",
    "PATCH": "update",
    "DELETE": "delete",
}

def check_access(user, element_key: str, action: str) -> bool:
    if not hasattr(user, "id"):
        return False
    element = BusinessElement.objects.filter(key=element_key).only("id").first()
    if not element:
        return False

    role_ids = UserRole.objects.filter(user_id=user.id).values_list("role_id", flat=True)

    if not role_ids:
        return False

    return AccessRule.objects.filter(
        role_id__in=role_ids,
        element_id=element.id,
        action=action,
        allow=True,
    ).exists()

class RBACPermission(BasePermission):
    def has_permission(self, request, view):
        element = getattr(view, "rbac_element", None)
        if not element:
            return True

        user = getattr(request, "auth_user", None)
        if not user:
            raise NotAuthenticated("No auth token")

        action = getattr(view, "rbac_action", None) or METHOD_TO_ACTION.get(request.method, "read")

        if check_access(user, element, action):
            return True

        raise PermissionDenied("RBAC: access denied")
