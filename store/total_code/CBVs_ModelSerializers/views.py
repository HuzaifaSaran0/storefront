from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
# These next 2 classes are used to serialize the data
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

# this is used to Beautify the status code
from rest_framework import status
# Create your views here.
from rest_framework.views import APIView

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product) # This will serialize the product object
        return Response(serializer.data) # This will return the serialized data
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CollectionList(APIView):
    def get(self, request):
        products = Collection.objects.annotate(products_count=Count('products')).all() # ANNOTATE is used to add a new field to the queryset
        # This will add a new field called products_count to the queryset which will count the number of products in the collection and that field would be accessed by products_count in the file of serializers.py
        serializer = CollectionSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    def put(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    