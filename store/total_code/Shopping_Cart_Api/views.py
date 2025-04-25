from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Collection, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer,CartItemSerializer , CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from django.db.models import Count
# from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter
from .pagination import DefaultPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() # queryset is used to get the products from the database
    serializer_class = ProductSerializer # serializer_class is used to serialize the product data
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # This will allow us to filter the products by collection and unit price
    filterset_class = ProductFilter # This will allow us to filter the products by collection and unit price
    # pagination_class = PageNumberPagination # This will allow us to paginate the products
    pagination_class = DefaultPagination # This will allow us to paginate the products
    search_fields = ['title', 'description'] # This will allow us to search the products by title and description
    ordering_fields = ['unit_price'] # This will allow us to Sort the products by unit price


    # def get_serializer_context(self):
    #     return {'request': self.request}

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk) # This will get the product or return 404 if not found
        if product.orderitem_set.exists(): # This will check if the product is associated with an order item
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # This will delete the product
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the product is deleted successfully
    

class CollectionViewSet(ModelViewSet):
    # queryset = Collection.objects.all()
    queryset = Collection.objects.annotate(products_count=Count('products')) # This will annotate the collection with the number of products in it
    # where annotate means to add a new field to the queryset
    serializer_class = CollectionSerializer

    def destroy(self, request, pk=None):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk) # This will get the collection or return 404 if not found

        if collection.products.count() > 0: # This will check if the collection contains products
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete() # This will delete the collection
        return Response(status=status.HTTP_204_NO_CONTENT) # This will return 204 No Content if the collection is deleted successfully
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['product_pk'] # pk = product_pk = product_primary_key
        get_object_or_404(Product, pk=product_id) # This will get the product or return 404 if not found
        return Review.objects.filter(product_id=product_id) # This will filter the reviews by product id
    # This is used to get the product id from the URL and pass it to the serializer context
    # so that we can use it in the serializer

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk'] # This will get the product id from the URL and pass it to the serializer context
        }


    # def get_queryset(self):
    #     product_id = self.kwargs['product_pk']
    #     get_object_or_404(Product, pk=product_id)
    #     return Review.objects.filter(product_id=product_id)
    
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    # queryset = Cart.objects.all()
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemsViewSet(ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects \
                .filter(cart_id=self.kwargs['cart_pk']) \
                .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    



