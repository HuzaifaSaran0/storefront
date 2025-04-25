from itertools import product
from pprint import pp
import pprint
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price', 'inventory', 'price_with_tax', 'collection']
        # fields = ['id', 'title', 'description', 'unit_price', 'inventory', 'price_with_tax', 'collection']
    #     read_only_fields = ['id', 'price_with_tax'] # This will make the id and price_with_tax fields read only
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all()) # This is Serializing the collection object
    #  PrimaryKeyRelatedField is used to serialize the foreign key field in the model
    #  It will return the id of the collection object instead of the whole object

    def calculate_price_with_tax(self, product: Product):
        return f"{product.unit_price * Decimal(1.1)} (Inc. VAT)"
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count'] # This will serialize the Collection model with the fields id and title

    id = serializers.IntegerField(read_only=True) # This will make the id field read only
    products_count = serializers.IntegerField(read_only=True) # This will count the number of products in the collection with 

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']
    
    # id = serializers.IntegerField(read_only=True) # This will make the id field read only
    # product_id = serializers.IntegerField(write_only=True) # This will make the product_id field write only
    def create(self, validated_data):
        product_id = self.context['product_id']
        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Invalid product ID'})
        
        return Review.objects.create(product_id=product_id, **validated_data)
        # here **validated_data is used to unpack the data and pass it to the create method of the Review model


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']  
      

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    # # product_title = serializers.CharField(source='product.title', read_only=True)
    # # product_price = serializers.DecimalField(source='product.unit_price', max_digits=6, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        # fields = ['id', 'quantity', 'total_price'] # This will serialize the CartItem model with the fields id, quantity and product
        fields = ['id', 'quantity', 'product', 'total_price']
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        # fields = ['id', 'total_price'] # This will serialize the Cart model with the fields id, items_count and total_price
        fields = ['id', 'total_price', 'items'] # This will serialize the Cart model with the fields id, items_count and total_price

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given Id was found.')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance   

    class Meta:
        model = CartItem
        fields = ['id','product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
