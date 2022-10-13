from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderList.as_view()),
    path('orders/<int:pk>/', views.OrderUpdateDelete.as_view()),
    path('orders/create/', views.OrderCreate.as_view()),
    path('orders/<int:pk>/update/', views.OrderUpdateDelete.as_view()),
    path('orders/<int:pk>/delete/', views.OrderUpdateDelete.as_view()),
]