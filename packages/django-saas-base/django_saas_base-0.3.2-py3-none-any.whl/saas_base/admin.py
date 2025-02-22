from django.contrib import admin
from .models import (
    Permission,
    Group,
    Member,
    UserEmail,
    get_tenant_model,
)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["name", "internal", "created_at"]


@admin.register(get_tenant_model())
class TenantAdmin(admin.ModelAdmin):
    list_display = ["pk", "slug", "owner", "expires_at", "created_at"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "invite_email", "status", "created_at"]


@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ["pk", "email", "primary", "verified", "created_at"]
