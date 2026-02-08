from django.db import models
from django.utils import timezone

from apps.accounts.models import User


class Role(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    key = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.key


class AccessRule(models.Model):
    ACTION_READ = "read"
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    ACTION_CHOICES = (
        (ACTION_READ, "read"),
        (ACTION_CREATE, "create"),
        (ACTION_UPDATE, "update"),
        (ACTION_DELETE, "delete"),
    )

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="rules")
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name="rules")
    action = models.CharField(max_length=16, choices=ACTION_CHOICES)
    allow = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("role", "element", "action")

    def __str__(self):
        return f"{self.role.slug}:{self.element.key}:{self.action} => {'allow' if self.allow else 'deny'}"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user_id} -> {self.role.slug}"
