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


@transaction.atomic
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
        if total is None:
            return 0
        return "%.2f" % Decimal(total)

    @transaction.atomic
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

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.isPile:
            raise SystemError("You cannot delete the pile.")
        if not self.isPile:
            transactions_to_transfer_to_pile = Transaction.objects.filter(stack=self)
            pile = Stack.objects.filter(isPile=True).first()
            for transaction in transactions_to_transfer_to_pile:
                transaction.stack = pile
                transaction.save()
        return super(Stack, self).delete(*args, **kwargs)

    @transaction.atomic
    def transfer_to(self, stack: Stack, amount: Decimal):
        """Transfer money from this stack to another stack. Generates two transactions."""
        if self == stack:
            raise SystemError("You cannot transfer money to the same stack.")
        if amount > Decimal(self.total):
            raise SystemError("You cannot transfer more money than you have.")
        if amount < 0:
            raise SystemError("You cannot transfer a negative amount.")
        if amount == 0:
            raise SystemError("You cannot transfer 0 money.")
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
        return source, destination


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

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.stack is None:
            self.stack = Stack.objects.get(isPile=True)
        return super(Transaction, self).save(*args, **kwargs)

    @transaction.atomic
    def split_transaction(self, stack_ammounts: dict[Stack, Decimal]):
        """Split a transaction into multiple transactions."""
        if self.split:
            raise SystemError("You cannot split a split transaction.")
        if self.transfer:
            raise SystemError("You cannot split a transfer transaction.")
        if self.split_from:
            raise SystemError("You cannot split a split transaction.")
        if len(stack_ammounts) < 2:
            raise ValueError("You must split a transaction into at least two stacks.")
        if self.amount < 0 and any(amount > 0 for amount in stack_ammounts.values()):
            raise ValueError(
                "You cannot split a negative transaction into positive amounts."
            )
        if self.amount > 0 and any(amount < 0 for amount in stack_ammounts.values()):
            raise ValueError(
                "You cannot split a positive transaction into negative amounts."
            )
        total = sum(stack_ammounts.values())
        if total != self.amount:
            raise ValueError(
                "The total of the split transactions must equal the original transaction amount."
            )
        for stack, amount in stack_ammounts.items():
            new_transaction = Transaction(
                date=self.date,
                amount=amount,
                description=self.description,
                transfer=self.transfer,
                stack=stack,
                split=False,
                split_from=self,
            )
            new_transaction.save()
        self.split = True
        self.save()
        return [self] + [list(Transaction.objects.filter(split_from=self).all())]

    @transaction.atomic
    def recombine_split(self):
        """Recombine a split transaction into a single transaction."""
        if not self.split:
            raise SystemError("You cannot recombine a non-split transaction.")
        for transaction in Transaction.objects.filter(split_from=self):
            transaction.delete()
        self.split = False
        self.save()
        return self

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.split:
            raise SystemError("You cannot delete a split transaction.")
        if self.transfer:
            raise SystemError("You cannot delete a transfer transaction.")
        return super(Transaction, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
