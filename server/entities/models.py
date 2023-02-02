from __future__ import annotations
from django.db import models
import uuid
from decimal import Decimal
from datetime import datetime
from django.db import models, transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from easy_tenants import tenant_context
from easy_tenants.models import TenantManager, TenantAwareAbstract


class Tenant(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def total(self):
        return Transaction.objects.all().aggregate(models.Sum("amount"))["amount__sum"]


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

    def save(self, *args, **kwargs):
        if not self.users_default_tenant:
            return super(TenantUser, self).save(*args, **kwargs)
        with transaction.atomic():
            TenantUser.objects.filter(users_default_tenant=True).update(
                users_default_tenant=False
            )
            return super(TenantUser, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("tenant", "user"),)


class Stack(TenantModel):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=31, blank=True, null=True)
    isPile = models.BooleanField(default=False, editable=False)
    goal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def total(
        self,
        datefrom: datetime = datetime(1900, 1, 1),
        dateto: datetime = datetime.now(),
    ):
        total = Transaction.objects.filter(stack=self, split=False).aggregate(
            models.Sum("amount")
        )["amount__sum"]
        return "%.2f" % Decimal(total)

    def save(self, *args, **kwargs):
        pile = Stack.objects.filter(isPile=True).first()
        if (
            self.isPile
            and self != pile
            and Stack.objects.filter(isPile=True).count() > 0
        ):
            raise SystemError("There can only be one pile per tenant.")

        if self == pile:
            self.isPile = True
        return super(Stack, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.isPile:
            raise SystemError("You cannot delete the pile.")
        return super(Stack, self).delete(*args, **kwargs)

    def transfer_to(self, stack: Stack, amount: Decimal):
        """Transfer money from this stack to another stack. Generates two transactions."""
        source = Transaction(
            date=datetime.now(),
            amount=amount * -1,
            description=f"Transfer from {self.name}",
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


class Transaction(TenantModel):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    stack = models.ForeignKey(Stack, on_delete=models.SET_NULL, null=True)
    transfer = models.BooleanField(default=False)
    split = models.BooleanField(default=False)
    split_from = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        indexes = [models.Index(fields=["date", "amount", "description"])]
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if self.stack is None:
            self.stack = Stack.objects.get(isPile=True)
        return super(Transaction, self).save(*args, **kwargs)
