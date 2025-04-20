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
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk) # This will get the product or return 404 if not found
        if product.orderitem_set.exists(): # This will check if the product is associated with an order item
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # This will delete the product
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the product is deleted successfully
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it
    serializer_class = CollectionSerializer


    def destroy(self, request, pk=None):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk) # This will get the collection or return 404 if not found

        if collection.products.count() > 0: # This will check if the collection contains products
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete() # This will delete the collection
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # This is used to get the product id from the URL and pass it to the serializer context
    # so that we can use it in the serializer
    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }



# MORE ADVANCED WAY TO DO THE SAME THING AS ABOVE (IF YOU WANT TO USE THIS COMMENTED CODE INSTEAD OF THE ABOVE CODE, THEN U HAVE TO USE COMMENTED CODE IN SERIALIZERS.PY FILE TOO)

# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer
#     # This is used to get the product id from the URL and pass it to the serializer context
#     # so that we can use it in the serializer
#     def get_serializer_context(self):
#         return {
#             'product_id': self.kwargs['product_pk']
#         }

#     def get_queryset(self):
#         product_id = self.kwargs['product_pk']
#         get_object_or_404(Product, pk=product_id)



#         return Review.objects.filter(product_id=product_id)