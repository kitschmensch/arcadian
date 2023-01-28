from __future__ import annotations
import decimal
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from easy_tenants import tenant_context
from easy_tenants.models import TenantManager, TenantAwareAbstract


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # encrypt this!!!


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=Tenant)
def tenant_created(instance, created, **kwargs):
    """Create a pile for the tenant when it is created."""
    with tenant_context(instance.tenant):
        if created and Stack.objects.filter(isPile=True).count() == 0:
            pile = Stack(name="Pile", isPile=True)
            pile.save()


class TenantUser(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Stack(TenantAwareAbstract):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    emoji = models.CharField(max_length=31, blank=True, null=True)
    listOrder = models.PositiveSmallIntegerField()
    isPile = models.BooleanField(default=False, editable=False)
    objects = TenantManager()

    class Meta:
        ordering = ["-listOrder"]

    def save(self, *args, **kwargs):
        with tenant_context(self.tenant):
            list_items = Stack.objects.all()
            if self.listOrder <= list_items.count():
                for item in list_items:
                    if item.listOrder >= self.listOrder:
                        item.listOrder += 1
                        item.save()
            else:
                self.listOrder = list_items.count() + 1
        super(Stack, self).save(*args, **kwargs)

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


def get_pile(tenant):
    with tenant_context(tenant):
        try:
            return Stack.objects.get(isPile=True)
        except:
            SystemError("No pile found. This should never happen.")


class Transaction(TenantAwareAbstract):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    stack = models.ForeignKey(
        Stack, on_delete=models.SET_DEFAULT, default=get_pile(tenant)
    )
    transfer = models.BooleanField(default=False)
    objects = TenantManager()

    class Meta:
        unique_together = (("date", "amount", "description"),)
        indexes = [models.Index(fields=["date", "amount", "description"])]
        ordering = ["-date"]
