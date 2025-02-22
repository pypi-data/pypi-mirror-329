from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from ..models import get_tenant_model, Member
from ..settings import saas_settings

__all__ = [
    'HasResourcePermission',
    'HasResourceScope',
    'IsTenantOwner',
]

TenantModel = get_tenant_model()

http_method_actions = {
    'GET': 'read',
    'HEAD': 'read',
    'POST': 'write',
    'PUT': 'write',
    'PATCH': 'write',
    'DELETE': 'admin',
}


class IsTenantOwner(BasePermission):
    def has_permission(self, request: Request, view):
        tenant_id = getattr(request, "tenant_id", None)
        if not tenant_id:
            return False
        try:
            tenant = TenantModel.objects.get_from_cache_by_pk(tenant_id)
            return request.user.pk == tenant.owner_id
        except TenantModel.DoesNotExist:
            return False


class HasResourcePermission(BasePermission):
    @staticmethod
    def get_resource_permissions(view, method):
        resource = getattr(view, 'resource_name', None)
        if not resource:
            return

        action = getattr(view, 'resource_action', None)
        if not action:
            method_actions = getattr(view, 'resource_http_method_actions', http_method_actions)
            action = method_actions.get(method)

        permission = saas_settings.PERMISSION_NAME_FORMATTER.format(
            resource=resource,
            action=action,
        )
        return [permission]

    @staticmethod
    def get_tenant(tenant_id):
        try:
            return TenantModel.objects.get_from_cache_by_pk(tenant_id)
        except TenantModel.DoesNotExist:
            return None

    @staticmethod
    def get_all_permissions(tenant_id, user_id):
        try:
            member = Member.objects.get_by_natural_key(tenant_id, user_id)
            if member.is_active:
                return member.get_all_permissions()
        except Member.DoesNotExist:
            return None

    def has_permission(self, request: Request, view):
        resource_permissions = self.get_resource_permissions(view, request.method)
        if not resource_permissions:
            return True

        # HasResourcePermission should apply to TenantEndpoint
        tenant_id = getattr(request, "tenant_id", None)
        if not tenant_id:
            return False

        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False

        # Tenant owner has all permissions
        if tenant.owner_id == request.user.pk:
            return True

        perms = self.get_all_permissions(tenant_id, request.user.pk)
        if not perms:
            return False

        for name in resource_permissions:
            if name in perms:
                return True
        return False


class HasResourceScope(BasePermission):
    @staticmethod
    def get_resource_scopes(view, method):
        if hasattr(view, 'get_resource_scopes'):
            resource_scopes = view.get_resource_scopes(method)
        elif hasattr(view, 'resource_scopes'):
            resource_scopes = view.resource_scopes
        else:
            resource_scopes = None
        return resource_scopes

    def has_permission(self, request: Request, view):
        resource_scopes = self.get_resource_scopes(view, request.method)
        if not resource_scopes:
            return True

        if request.auth is None:
            return True

        scope = getattr(request.auth, 'scope', '')
        if scope == "__all__":
            return True

        token_scopes = set(scope.split())
        for rs in resource_scopes:
            if set(rs.split()).issubset(token_scopes):
                return True
        return False
