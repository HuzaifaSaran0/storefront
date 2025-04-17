from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
# from .models import Product

router = SimpleRouter()
router.register('first', views.firstViewSet, basename='first')
urlpatterns = router.urls



# URLConf
# urlpatterns = [
#     # path('first/', views.first),
#     path('first/', views.first.as_view()),
#     path('first/<int:pk>/', views.first_details.as_view()),
#     # path('products/<int:id>/', views.product_detail),
# ]
