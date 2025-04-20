from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('collections/', views.CollectionList.as_view(), name='collection-list'),
    path('collections/<int:id>/', views.CollectionDetail.as_view(), name='collection-detail'),
]