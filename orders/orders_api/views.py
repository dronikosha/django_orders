from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from main.models import Order
from .permissions import IsOwnerOrReadOnly
from .serializers import OrderSerializer
from .paginations import CustomPagination


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all().reverse()
    pagination_class = CustomPagination
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().reverse()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]


class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
