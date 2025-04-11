from rest_framework import serializers 
from decimal import Decimal
from store.models import Product,Collection, Reviews, Cart
class CollectionSerializer(serializers.Serializer) :
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ["id" , "title" , "slug","inventory" ,"description" ,  "unit_price" , "price_with_tax" , "collection"] 
        

    # id = serializers.IntegerField()
    # title  = serializers.CharField(max_length=255) 
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2) 
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  
    # collection = CollectionSerializer() 
    
    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1) 
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields  = ["id" , "date" ,"name" , "description" ]
    def create(self , validated_data):
        product_id  = self.context['product_id']
        return Reviews.objects.create(product_id = product_id , **validated_data)
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    class Meta:
        model = Cart
        fields = ['id']
    

    

    