# API URLS
from django.urls import path

from entities.views import (
    TenantUserListAPIView,
    TenantUserRetrieveUpdateDestroyAPIView,
    TenantAPIView,
    StackListCreateAPIView,
    StackDetailAPIView,
    StackTransfer,
    TransactionListCreateAPIView,
    TransactionDetailAPIView,
    split_transaction,
    recombine_transaction,
)

urlpatterns = [
    path("tenants/", TenantUserListAPIView.as_view(), name="TenantUser"),
    path(
        "tenants/<int:id>/",
        TenantAPIView.as_view(),
        name="ChangeDefaultTenant",
    ),
    path("stacks/", StackListCreateAPIView.as_view(), name="Stacks"),
    path("stacks/<int:pk>/", StackDetailAPIView.as_view(), name="Stack"),
    path("stacks/<int:frm>/transferto/<int:to>", StackTransfer, name="Stack Transfer"),
    path("transactions/", TransactionListCreateAPIView.as_view(), name="Transactions"),
    path(
        "transactions/<int:pk>/",
        TransactionDetailAPIView.as_view(),
        name="Transaction",
    ),
    path("transactions/<int:id>/split", split_transaction, name="Split Transaction"),
    path(
        "transactions/<int:id>/recombine",
        recombine_transaction,
        name="Recombine Transaction",
    ),
]
