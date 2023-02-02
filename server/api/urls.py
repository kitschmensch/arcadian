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
]
