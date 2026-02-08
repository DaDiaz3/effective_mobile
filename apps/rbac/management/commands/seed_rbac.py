from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.rbac.models import Role, BusinessElement, AccessRule, UserRole

User = get_user_model()


class Command(BaseCommand):
    help = "Seed RBAC demo data"

    def handle(self, *args, **kwargs):
        docs, _ = BusinessElement.objects.get_or_create(
            key="documents",
            defaults={"name": "Documents", "description": "Mock documents API"},
        )

        admin_role, _ = Role.objects.get_or_create(name="Admin", slug="admin")
        viewer_role, _ = Role.objects.get_or_create(name="Viewer", slug="viewer")

        for action in ["read", "create", "update", "delete"]:
            AccessRule.objects.get_or_create(
                role=admin_role, element=docs, action=action, defaults={"allow": True}
            )

        AccessRule.objects.get_or_create(
            role=viewer_role, element=docs, action="read", defaults={"allow": True}
        )

        u = User.objects.order_by("id").first()
        if u:
            UserRole.objects.get_or_create(user=u, role=admin_role)
            self.stdout.write(self.style.SUCCESS(f"Attached 'admin' role to user id={u.id}"))
        else:
            self.stdout.write(self.style.WARNING("No users found, seeded only RBAC dictionaries"))

        self.stdout.write(self.style.SUCCESS("RBAC seeded."))
