from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from .models import Tenant, Stack, Transaction, TenantUser
from .serializers import (
    TenantSerializer,
    TenantUserSerializer,
    StackSerializer,
    TransactionSerializer,
)


class TenantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print(request.user)
        queryset = self.get_queryset().filter(tenantuser__user=request.user)
        serializer = TenantSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TenantUserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TenantUserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    depth = 1

    def get_queryset(self):
        return TenantUser.objects.filter(user=self.request.user)


class StackListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
