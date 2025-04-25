from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products') # basename is used to create a unique name for the viewset like products-list
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product') 
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# difference between lookup and basename is that lookup is used to get the id of the product in the url and basename is used to create a unique name for the viewset like products-list

# products_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
# products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemsViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls


