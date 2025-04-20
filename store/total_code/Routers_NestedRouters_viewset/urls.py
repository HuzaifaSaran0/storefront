from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet

router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet, basename='collections')

products_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls

# https://medium.com/@sunilnepali844/nested-routers-in-django-rest-framework-7d6a5a1cc8f0#:~:text=In%20
# BEST TUTORIAL DOCUMENTATION FOR NESTED ROUTERS