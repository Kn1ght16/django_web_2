from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('records/', views.RecordListView.as_view(), name='records_list'),
    path('records/<slug:slug>/', views.RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', views.RecordCreateView.as_view(), name='record_create'),
    path('product/item/<int:pk>/', views.ProductItemView.as_view(), name='product_item'),
    path('product/create/', views.create_product, name='product_create'),
    path('product/update/<int:pk>/', views.update_product, name='product_update'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
]