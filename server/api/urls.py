# API URLS
from django.urls import path

from entities.serializers import TenantSerializer
from entities.views import (
    TenantListCreateAPIView,
    TenantUserListCreateAPIView,
    StackListCreateAPIView,
    TransactionListCreateAPIView,
)

urlpatterns = [
    path("tenants/", TenantListCreateAPIView.as_view(), name="Tenants"),
    path("tenants/user", TenantUserListCreateAPIView.as_view(), name="TenantUser"),
    path("stacks/", StackListCreateAPIView.as_view(), name="Stacks"),
    path("transactions/", TransactionListCreateAPIView.as_view(), name="Transactions"),
]
