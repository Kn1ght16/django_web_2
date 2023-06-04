from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<int:product_id>/', views.Product, name='product'),
]