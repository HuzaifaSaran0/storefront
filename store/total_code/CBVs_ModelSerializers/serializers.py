from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price', 'inventory', 'price_with_tax', 'collection']
        read_only_fields = ['id', 'price_with_tax'] # This will make the id and price_with_tax fields read only
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all()) # This is Serializing the collection object

    def calculate_price_with_tax(self, product: Product):
        return f"{product.unit_price * Decimal(1.1)} (Inc. VAT)"
    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    id = serializers.IntegerField(read_only=True) # This will make the id field read only
    products_count = serializers.IntegerField(read_only=True) # This will count the number of products in the collection with 

    



