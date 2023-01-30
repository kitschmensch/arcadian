from rest_framework import serializers
from .models import Tenant, TenantUser, Stack, Transaction


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ("id", "name", "total")
        read_only_fields = ["id", "total"]


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "name", "creator"]
        read_only_fields = ["id", "creator"]


class TenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ["tenant_id", "users_default_tenant"]
        read_only_fields = ["tenant_id", "tenant"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("date", "amount", "description", "stack")
        read_only_fields = ["description"]
