from rest_framework import serializers
from .models import Product, Collection, Review
# for converting decimal to integer
from decimal import Decimal



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # fields = '__all__' # This will serialize all the fields in the model

    # WE HAVE TO WRITE THESE BELOW GIVEN FIELDS IF WE DON'T USE Meta CLASS AND MODELSERIALIZER INSTEAD OF SERIALIZER
    # id = serializers.IntegerField()
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    # collection = serializers.StringRelatedField()
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all()) # This is Serializing the collection object

    def calculate_price_with_tax(self, product: Product):
        return f"{product.unit_price * Decimal(1.1)} (Inc. VAT)"

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField(read_only=True) # This will count the number of products in the collection


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    



