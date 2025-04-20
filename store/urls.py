from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

from rest_framework_nested import routers

router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls






# using generic views + mixins
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from .views import ProductViewSet, CollectionViewSet, ReviewViewSet



# Create a router and register our viewset with it.
# router = DefaultRouter()
# router.register('products', ProductViewSet, basename='products')
# urlpatterns = router.urls # This will automatically generate the URL patterns for the viewset






# from .models import Product
# from rest_framework.routers import SimpleRouter
# from rest_framework_nested import routers


# # Now Nested Routers to get more functionalities
# router = routers.DefaultRouter()
# router.register('products', views.product_list_view, basename='products')
# router.register('collections', views.collection_list_view, basename='collections')


# # Child or nested routers
# products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# products_router.register('reviews', views.ReviewViewSet, basename='product-reviews') # Registering child router for reviews



# urlpatterns = router.urls + products_router.urls




# SIMPLE ROUTER with VIEWSET
# routers = SimpleRouter()
# routers.register('products', views.product_list_view, basename='products')
# routers.register('collections', views.collection_list_view, basename='collections')
# urlpatterns = routers.urls

# URLConf
