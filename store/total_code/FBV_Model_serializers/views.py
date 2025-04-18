# THE MAJOR DIFFERENCE BETWEEN FBV PLUS SERIALIZERS AND FBV WITH MODEL SERIALIZERS
# FBV with Serializer means you manually define all fields and also write the create() and update() methods yourself.
# FBV with ModelSerializer automatically generates fields and those methods based on your model, saving you time and code.
# Serializer gives more control and flexibility for custom logic, while ModelSerializer is best for standard CRUD.
# Both work with FBVs, but ModelSerializer is more efficient for typical model-based APIs.
# Use Serializer when you need customization; use ModelSerializer when speed and simplicity matter.


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


@api_view(['GET', 'POST']) # This is a decorator that will allow us to use the function as a view
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product) # This will serialize the product object
        return Response(serializer.data) # This will return the serialized data
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        products = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def collection_details(request, id):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    