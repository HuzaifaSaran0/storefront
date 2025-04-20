from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count
# from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter
from .pagination import DefaultPagination
# from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # This will allow us to filter the products by collection and unit price
    filterset_class = ProductFilter # This will allow us to filter the products by collection and unit price
    # pagination_class = PageNumberPagination # This will allow us to paginate the products
    pagination_class = DefaultPagination # This will allow us to paginate the products
    search_fields = ['title', 'description'] # This will allow us to search the products by title and description
    ordering_fields = ['unit_price'] # This will allow us to order the products by unit price


    def get_serializer_context(self):
        return {'request': self.request}

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

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        get_object_or_404(Product, pk=product_id)
        return Review.objects.filter(product_id=product_id)
    

    



# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id' # This will use the id field to look up the product

#     def delete(self, request, *args, **kwargs):
#         product = self.get_object() # This will get the product object
#         if product.orderitem_set.exists(): # This will check if the product is associated with an order item    
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete() # This will delete the product
#         return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the product is deleted successfully
    
    
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it

#     serializer_class = CollectionSerializer

#     lookup_field = 'id' # This will use the id field to look up the collection


#     def delete(self, request, *args, **kwargs):
#         collection = self.get_object() # This will get the collection object

#         if collection.products.count() > 0: # This will check if the collection contains products
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete() # This will delete the collection
#         return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    




# class CollectionDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it

#     serializer_class = CollectionSerializer

#     lookup_field = 'id' # This will use the id field to look up the collection

#     def get(self, request, id):
#         return self.retrieve(request, id) # This will return the collection details
    

#     def put(self, request, id):
#         return self.update(request, id) # This will update the collection details
    

#     def delete(self, request, id):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id) # This will get the collection or return 404 if not found
#         if collection.products.count() > 0: # This will check if the collection contains products
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete() # This will delete the collection
#         return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    
    

# class product_list_view(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def destroy(self, request, pk=None):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.exists():
#             return Response(
#                 {'error': 'Product cannot be deleted because it is associated with an order item'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class collection_list_view(ModelViewSet):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

#     def destroy(self, request, pk=None):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.exists():
#             return Response(
#                 {'error': 'Collection cannot be deleted because it contains products'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ReviewViewSet(ModelViewSet):
#     # queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     # This is used to get the product id from the URL and pass it to the serializer context 
#     # so that we can use it in the serializer
#     def get_serializer_context(self):
#         return {
#             'product_id': self.kwargs['product_pk']
#         }

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])



# @api_view(['GET', 'POST']) # This is a decorator that will allow us to use the function as a view
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data) # This will deserialize the data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data) # This will print the deserialized validated data
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # if serializer.is_valid():
        #     return Response('OK')
        #     # serializer.save()
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)
  


# @api_view() 
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product) # This will serialize the product object
#         return Response(serializer.data) # This will return the serialized data
#     except Product.DoesNotExist:
#         return Response({'Error': 'Product not found'}, status=404)

# @api_view(['GET', 'PUT', 'DELETE']) 
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product) # This will serialize the product object
#         return Response(serializer.data) # This will return the serialized data
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         products = Collection.objects.annotate(products_count=Count('products')).all() 
#         serializer = CollectionSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# @api_view(['GET', 'POST', 'DELETE'])
# def collection_details(request, id):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=id)
#     print(collection)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
