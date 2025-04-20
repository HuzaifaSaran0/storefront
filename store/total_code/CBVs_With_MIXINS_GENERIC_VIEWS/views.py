from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count
# from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
# from rest_framework import generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class ProductList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        return self.list(request) # This will return the list of products
    
    def post(self, request):
        return self.create(request) # This will create a new product

class ProductDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    lookup_field = 'id' # This will use the id field to look up the product

    def get(self, request, id):
        return self.retrieve(request, id) # This will return the product details
    
    def put(self, request, id):
        return self.update(request, id) # This will update the product details
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id) # This will get the product or return 404 if not found
        if product.orderitem_set.count() > 0: # This will check if the product is associated with an order item
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # This will delete the product
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the product is deleted successfully
    

    
    
class CollectionList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it
    serializer_class = CollectionSerializer

    def get(self, request):
        return self.list(request) # This will return the list of collections
    
    def post(self, request):
        return self.create(request) # This will create a new collection
    




class CollectionDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it

    serializer_class = CollectionSerializer

    lookup_field = 'id' # This will use the id field to look up the collection

    def get(self, request, id):
        return self.retrieve(request, id) # This will return the collection details
    

    def put(self, request, id):
        return self.update(request, id) # This will update the collection details
    

    def delete(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id) # This will get the collection or return 404 if not found
        if collection.products.count() > 0: # This will check if the collection contains products
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete() # This will delete the collection
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    
    
