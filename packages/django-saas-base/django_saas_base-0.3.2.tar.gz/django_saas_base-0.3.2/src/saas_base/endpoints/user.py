from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from ..drf.views import AuthenticatedEndpoint
from ..models import UserEmail, Member
from ..serializers.user import (
    UserSerializer,
    UserEmailSerializer,
    UserPasswordSerializer,
)
from ..serializers.member import UserTenantsSerializer


class UserEndpoint(AuthenticatedEndpoint):
    resource_scopes = ["user", "user:profile"]
    serializer_class = UserSerializer

    def get(self, request: Request):
        """Retrieve current user information."""
        serializer: UserSerializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserPasswordEndpoint(AuthenticatedEndpoint):
    resource_scopes = ["user:password"]
    serializer_class = UserPasswordSerializer

    def post(self, request: Request, *args, **kwargs):
        """Update current user's password"""
        serializer: UserPasswordSerializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


class UserEmailListEndpoint(ListModelMixin, AuthenticatedEndpoint):
    resource_scopes = ["user:email"]
    pagination_class = None
    serializer_class = UserEmailSerializer

    def get_queryset(self):
        return UserEmail.objects.filter(user=self.request.user).all()

    def get(self, request: Request, *args, **kwargs):
        """List all the current user's emails."""
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        # add email
        pass


class UserTenantsEndpoint(ListModelMixin, AuthenticatedEndpoint):
    serializer_class = UserTenantsSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = Member.objects.select_related('tenant')
        queryset = queryset.prefetch_related('groups', 'permissions', 'groups__permissions')
        queryset = queryset.filter(user=self.request.user)

        if status == 'all':
            return queryset.all()
        if status == 'waiting':
            queryset = queryset.filter(status=Member.InviteStatus.WAITING)
        else:
            queryset = queryset.filter(status=Member.InviteStatus.ACTIVE)
        return queryset.all()

    def get(self, request: Request, *args, **kwargs):
        """List all the current user's tenants."""
        return self.list(request, *args, **kwargs)
