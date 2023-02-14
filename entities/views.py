from datetime import datetime
from dateutil import parser
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from rest_framework import generics, permissions, authentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from typing import Dict, List
import csv
from rest_framework import status
from rest_framework.parsers import BaseParser
from rest_framework.views import APIView


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
    lookup_field = "id"


class TenantUserListAPIView(generics.ListAPIView):
    serializer_class = TenantUserSerializer

    def get_queryset(self):
        return TenantUser.objects.filter(user=self.request.user)


class TenantUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantUserSerializer
    lookup_field = "tenant_id"

    def get_queryset(self):
        return TenantUser.objects.filter(user=self.request.user)


class StackListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stack.objects.all().order_by("position")
    serializer_class = StackSerializer


class StackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer


@api_view(["GET", "POST"])
def StackTransfer(request, frm, to):
    amount = request.data.get("amount", None)
    from_stack = Stack.objects.get(id=frm)
    to_stack = Stack.objects.get(id=to)
    response = from_stack.transfer_to(stack=to_stack, amount=amount)
    return Response(True)


@api_view(["POST"])
def StackMove(request, stack_id, position):
    p = position
    n = Stack.objects.get(id=stack_id).position
    if p > Stack.objects.count():
        return Response(status=400, data="Position out of range")
    if p == n:
        return Response(True)
    if p < n:
        for stack in Stack.objects.filter(position__gte=p, position__lt=n):
            if stack.id == stack_id:
                continue
            stack.position += 1
            stack.save(nested=True)
    if p > n:
        for stack in Stack.objects.filter(position__gt=n, position__lte=p):
            if stack_id == stack.id:
                continue
            stack.position -= 1
            stack.save(nested=True)
    stack = Stack.objects.get(id=stack_id)
    stack.position = p
    stack.save(nested=True)
    return Response(True)


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.filter(
        Q(transfer=True) & Q(amount__gt=0) | Q(transfer=False)
    )
    serializer_class = TransactionSerializer
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


@api_view(["POST"])
def split_transaction(request, id):
    stack_amounts = request.data
    transaction_to_split = Transaction.objects.get(id=id)
    transaction_to_split.split_transaction(stack_amounts)
    return Response()


@api_view(["POST"])
def recombine_transaction(request, id):
    transaction_to_recombine = Transaction.objects.get(id=id)
    transaction_to_recombine.recombine()
    return Response()


@api_view(["POST"])
def autoTransfer(request):
    stacks = Stack.objects.all()
    pile = Stack.objects.get(isPile=True)
    for stack in stacks:
        if stack.isPile:
            continue
        if stack.autotransfer == 0 or stack.autotransfer is None:
            continue
        pile.transfer_to(stack, stack.autotransfer)
    return Response(204)


class CSVTextParser(BaseParser):

    media_type = "text/csv"

    def parse(self, stream, media_type=None, parser_context=None) -> List[List]:
        """
        Return a list of lists representing the rows of a CSV file.
        """
        # return list(csv.reader(stream, dialect='excel'))

        charset = "utf-8"
        media_type_params = dict(
            [param.strip().split("=") for param in media_type.split(";")[1:]]
        )
        charset = media_type_params.get("charset", "utf-8")
        dialect = media_type_params.get("dialect", "excel")
        txt = stream.read().decode(charset)
        csv_table = list(csv.reader(txt.splitlines(), dialect=dialect))
        return csv_table


class CsvCreate(APIView):
    parser_classes = (CSVTextParser,)

    def post(self, request, version=None):
        content_type = request.content_type.split(";")[0].strip()
        encoding = "utf-8"

        if content_type == "text/csv":
            csv_table = request.data
            for x in csv_table:
                if x[0] == "Date":
                    continue
                date = x[0] + "T" + x[1]
                # rule logic here!!
                new_transaction = Transaction(
                    date=date,
                    amount=x[2],
                    description=x[4],
                )
                new_transaction.save()
            return Response(csv_table, status=status.HTTP_200_OK)

        elif content_type == "multipart/form-data":
            fh = request.data.get("file", None)
            csv_table = fh.read().decode(encoding)
            return Response(csv_table, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
