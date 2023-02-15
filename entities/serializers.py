from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.response import Response
from .models import Tenant, TenantUser, Stack, Transaction
from django.db import models
from decimal import Decimal


class StackSerializer(serializers.ModelSerializer):
    spent = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Stack
        fields = (
            "id",
            "isPile",
            "name",
            "goal",
            "total",
            "spent",
            "saved",
            "budget",
            "autotransfer",
            "position",
        )
        read_only_fields = [
            "id",
            "total",
            "spent",
            "saved",
        ]

    def get_spent(self, obj):
        datefrom = self.context["request"].query_params.get("datefrom", None)
        dateto = self.context["request"].query_params.get("dateto", None)
        if datefrom is None:
            datefrom = datetime.now().replace(day=1)
        if dateto is None:
            dateto = datetime.now()
        spent_total = Transaction.objects.filter(
            stack=obj,
            date__gte=datefrom,
            date__lte=dateto,
            amount__lt=0,
            split=False,
            transfer=False,
        ).aggregate(models.Sum("amount"))["amount__sum"]
        if spent_total is None:
            spent_total = 0
            return 0
        return "%.2f" % Decimal(spent_total)

    def get_saved(self, obj):
        datefrom = self.context["request"].query_params.get("datefrom", None)
        dateto = self.context["request"].query_params.get("dateto", None)
        if datefrom is None:
            datefrom = datetime(1900, 1, 1)
        if dateto is None:
            dateto = datetime.now()
        saved_total = Transaction.objects.filter(
            stack=obj, date__gte=datefrom, date__lte=dateto, amount__gt=0, split=False
        ).aggregate(models.Sum("amount"))["amount__sum"]
        if saved_total is None:
            saved_total = 0
            return 0
        return "%.2f" % Decimal(saved_total)


class TenantUserSerializer(serializers.ModelSerializer):
    tenant_id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = TenantUser
        fields = (
            "tenant_id",
            "name",
            "users_default_tenant",
        )

    def get_tenant_id(self, obj):
        return obj.tenant.id

    def get_name(self, obj):
        return obj.tenant.name


class TenantSerializer(serializers.ModelSerializer):
    spent = serializers.SerializerMethodField()
    earned = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = ["id", "name", "spent", "earned", "total"]
        read_only_fields = ["id"]

    def get_spent(self, obj):
        datefrom = self.context["request"].query_params.get("datefrom", None)
        dateto = self.context["request"].query_params.get("dateto", None)
        if datefrom is None:
            datefrom = datetime(1900, 1, 1)
        if dateto is None:
            dateto = datetime.now()
        spent_total = Transaction.objects.filter(
            date__gte=datefrom,
            date__lte=dateto,
            amount__lt=0,
            split=False,
            transfer=False,
        ).aggregate(models.Sum("amount"))["amount__sum"]
        if spent_total is None:
            return 0

        return "%.2f" % Decimal(spent_total)

    def get_earned(self, obj):
        datefrom = self.context["request"].query_params.get("datefrom", None)
        dateto = self.context["request"].query_params.get("dateto", None)
        if datefrom is None:
            datefrom = datetime(1900, 1, 1)
        if dateto is None:
            dateto = datetime.now()
        saved_total = Transaction.objects.filter(
            date__gte=datefrom,
            date__lte=dateto,
            amount__gt=0,
            split=False,
            transfer=False,
        ).aggregate(models.Sum("amount"))["amount__sum"]
        if saved_total is None:
            saved_total = 0
        return "%.2f" % Decimal(saved_total)


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format=None, input_formats=None)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "amount",
            "description",
            "stack",
            "transfer",
            "split",
            "split_from",
        ]
        read_only_fields = ["id"]
