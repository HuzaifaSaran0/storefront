from django.urls import path
from . import views
# from .models import Product
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


# Now Nested Routers to get more functionalities
router = routers.DefaultRouter()
router.register('products', views.product_list_view, basename='products')
router.register('collections', views.collection_list_view, basename='collections')


# Child or nested routers
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews') # Registering child router for reviews



urlpatterns = router.urls + products_router.urls




# SIMPLE ROUTER with VIEWSET
# routers = SimpleRouter()
# routers.register('products', views.product_list_view, basename='products')
# routers.register('collections', views.collection_list_view, basename='collections')
# urlpatterns = routers.urls

# URLConf
# urlpatterns = [
#     path('products/', views.product_list),
#     path('products/<int:id>/', views.product_detail),
#     path('collections/', views.collection_list),
#     path('collections/<int:id>/', views.collection_details),
# ]
