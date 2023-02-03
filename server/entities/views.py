from rest_framework import generics, permissions, authentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import filters
from typing import TypedDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tenant, Stack, Transaction, TenantUser
from .serializers import (
    TenantSerializer,
    TenantUserSerializer,
    StackSerializer,
    TransactionSerializer,
)


class StandardResultsSetPagination(LimitOffsetPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


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


class TenantAPIView(generics.RetrieveAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


class TenantUserListAPIView(generics.ListAPIView):
    serializer_class = TenantUserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TenantUser.objects.filter(user=self.request.user)


class TenantUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantUserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "tenant_id"

    def get_queryset(self):
        return TenantUser.objects.filter(user=self.request.user)


class StackListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class StackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET", "POST"])
def StackTransfer(request, frm, to):
    amount = request.data.get("amount", None)
    from_stack = Stack.objects.get(id=frm)
    to_stack = Stack.objects.get(id=to)
    response = from_stack.transfer_to(stack=to_stack, amount=amount)
    return Response(response)


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.SessionAuthentication]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "date": ["gte", "lte"],
        "amount": ["gte", "lte"],
        "stack__id": ["exact"],
    }
    search_fields = ["description"]


class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
def split_transaction(request, id):
    stack_amounts = request.data
    stack = Stack.objects.get(id=id)
    processed_stack_amounts = {}
    for key, value in stack_amounts.items():
        stack = Stack.objects.get(id=key)
        processed_stack_amounts.update({stack: value})
    response = stack.split(processed_stack_amounts)
    return Response(response)


@api_view(["POST"])
def recombine_transaction(request, id):
    stack = Stack.objects.get(id=id)
    response = stack.recombine()
    return Response(response)
