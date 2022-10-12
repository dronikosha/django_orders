from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('order/<int:order_id>', views.order, name='order'),
    path('update/<int:order_id>', views.update, name='update'),
    path('delete/<int:order_id>', views.delete, name='delete'),
]
