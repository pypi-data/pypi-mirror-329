from rest_framework import serializers
from ..models import get_tenant_model
from ..models import Permission, Group
from ..signals import (
    before_create_tenant,
    before_update_tenant,
)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'description', 'internal']


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_tenant_model()
        exclude = ['owner']

    def create(self, validated_data):
        before_create_tenant.send(self.__class__, data=validated_data, **self.context)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        before_update_tenant.send(self.__class__, tenant=instance, data=validated_data, **self.context)
        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'managed']


class GroupPermissionSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'managed']
