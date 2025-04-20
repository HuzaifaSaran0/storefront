from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count
# from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
# from rest_framework import generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id' # This will use the id field to look up the product

    def delete(self, request, *args, **kwargs):
        product = self.get_object() # This will get the product object
        if product.orderitem_set.exists(): # This will check if the product is associated with an order item    
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # This will delete the product
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the product is deleted successfully
    
    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it

    serializer_class = CollectionSerializer

    lookup_field = 'id' # This will use the id field to look up the collection


    def delete(self, request, *args, **kwargs):
        collection = self.get_object() # This will get the collection object

        if collection.products.count() > 0: # This will check if the collection contains products
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete() # This will delete the collection
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    
