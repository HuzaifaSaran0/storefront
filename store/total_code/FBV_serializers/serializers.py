from rest_framework import serializers
from .models import Product, Collection
# for converting decimal to integer
from decimal import Decimal



class ProductSerializer(serializers.Serializer):

    # WE HAVE TO WRITE THESE BELOW GIVEN FIELDS IF WE DON'T USE Meta CLASS AND MODELSERIALIZER INSTEAD OF SERIALIZER
    id = serializers.IntegerField(read_only=True) # This will make the id field read only
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all()) # This is Serializing the collection object

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def calculate_price_with_tax(self, product: Product):
        return f"{product.unit_price * Decimal(1.1)} (Inc. VAT)"
    
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) # This will make the id field read only
    title = serializers.CharField(max_length=255)
    # featured_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False) # This will serialize the featured product object
    products_count = serializers.IntegerField(read_only=True) # This will count the number of products in the collection
    
    def create(self, validated_data):
        return Collection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
