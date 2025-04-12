from rest_framework import serializers 
from decimal import Decimal
from store.models import Product,Collection, Reviews, Cart , CartItem
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
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id" , "title" , "unit_price"] 

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cartitem):
        return cartitem.product.unit_price * cartitem.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity' , "total_price"]
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many=True , read_only=True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self,cart): 
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()]) 

    
    
    class Meta:
        model = Cart
        fields = ['id', "items" , "total_price"]
class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id" , "quantity" , "product_id"]
    product_id = serializers.IntegerField()
    def save(self, **kwargs):
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        cart_id = self.context["cart_id"]
        def validate_product_id(value):
            if not Product.objects.filter(pk=value).exists():
                raise serializers.ValidationError("Product does not exist.")
            return value
        try : 
            cart_item = CartItem.objects.get(product_id = product_id , cart_id = cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
             self.instance = CartItem.objects.create(cart_id = cart_id , product_id = product_id , quantity = quantity)
           
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id' ,"quantity"]
    class UpdateCartItemSerializer():
        class Meta:
            model = CartItem
            fields = ["quantity"]


    

    