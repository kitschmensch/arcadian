from __future__ import annotations
from django.db import models
import uuid
import decimal
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from easy_tenants import tenant_context
from easy_tenants.models import TenantManager, TenantAwareAbstract


class Tenant(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


@receiver(post_save, sender=Tenant)
def tenant_created(instance, created, **kwargs):
    """Create a pile for the tenant when it is created."""
    with tenant_context(instance):
        if created and Stack.objects.filter(isPile=True).count() == 0:
            pile = Stack(name="Pile", isPile=True)
            pile.save()
        if created and TenantUser.objects.filter(tenant=instance).count() == 0:
            tenant_user = TenantUser(
                tenant=instance, user=instance.creator, users_default_tenant=True
            )
            tenant_user.save()


class TenantModel(TenantAwareAbstract):
    tenant = models.ForeignKey(to=Tenant, on_delete=models.CASCADE)

    objects = TenantManager()

    class Meta:
        abstract = True


class TenantUser(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users_default_tenant = models.BooleanField(default=False)


@receiver(pre_save, sender=TenantUser)
def ensure_one_default_tenant(instance, **kwargs):
    if instance.users_default_tenant:
        old_default = TenantUser.objects.filter(users_default_tenant=True).first()
        if instance == old_default:
            pass
        else:
            old_default(users_default_tenant=False)
            old_default.save()
    else:
        if TenantUser.objects.filter(users_default_tenant=True).count() == 1:
            raise SystemError("There must be one default tenant per user.")


class Stack(TenantModel):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=31, blank=True, null=True)
    isPile = models.BooleanField(default=False, editable=False)

    @property
    def total(self):
        """Sum all transactions for this stack."""
        with tenant_context(self.tenant):
            return Transaction.objects.filter(stack=self).aggregate(
                models.Sum("amount")
            )["amount__sum"]

    def transfer_to(self, stack: Stack, amount: decimal.Decimal):
        """Transfer money from this stack to another stack. Generates two transactions."""
        with tenant_context(self.tenant):
            source = Transaction(
                date=datetime.now(),
                amount=amount * -1,
                description=f"Transfer From {self.name}",
                transfer=True,
                stack=self,
            )
            destination = Transaction(
                date=datetime.now(),
                amount=amount,
                description=f"Transfer to {stack.name}",
                transfer=True,
                stack=stack,
            )
            source.save()
            destination.save()


@receiver(pre_save, sender=Stack)
def ensure_one_pile_per_tenant(instance, **kwargs):
    """Ensure that there is only one pile per tenant."""
    if instance.isPile:
        with tenant_context(instance.tenant):
            if Stack.objects.filter(isPile=True).count() > 0:
                raise SystemError("There can only be one pile per tenant.")


class Transaction(TenantModel):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    stack = models.ForeignKey(Stack, on_delete=models.SET_NULL, null=True)
    transfer = models.BooleanField(default=False)

    class Meta:
        unique_together = (("date", "amount", "description", "tenant"),)
        indexes = [models.Index(fields=["date", "amount", "description"])]
        ordering = ["-date"]


@receiver(pre_save, sender=Transaction)
def get_pile(sender, instance, **kwargs):
    if instance.stack is None:
        with tenant_context(instance.tenant):
            instance.stack = Stack.objects.get(isPile=True)
