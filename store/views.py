from django.shortcuts import get_object_or_404, render 
from django.http import HttpResponse 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin


from store.filters import ProductFilter
from .models import Product ,Reviews 
from .serializers import ProductSerializer , ReviewSerializer ,CartSerializer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView 
from rest_framework.viewsets import ModelViewSet , GenericViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title' , 'description']
    OrderingFilter = ["unit_price"]
    def get_serializer_context(self, *args, **kwargs):
        return { 'request' : self.request }
    
    def delete(self,request , id):
        product = get_object_or_404(Product, pk = id)
        if product.orderitems.count() > 0 : 
            return Response({"error" : "Product cannot be deleted because it is associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class ProductList(APIView) : 
    def get(self,request) :
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def post(self , request): 
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True) 
        return Response(serializer.data)


class ProductDetail(APIView): 
    def get(self , request, id):
        product  = get_object_or_404(Product , pk =id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self , request , id):
        product  = get_object_or_404(Product , pk =id)
        serializer = ProductSerializer(product , data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data , status= status.HTTP_201_CREATED)


    
    


class ReviewViewSet(ModelViewSet):
    queyset  = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Reviews.objects.filter(product_id=product_id)
    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']} 
class CartViewSet(CreateModelMixin , GenericViewSet):
    queryset = Product.objects.all() 
    serializer_class = CartSerializer




        
    
    # try:
    #     product = Product.objects.get(id=id) 
    #     serializer = ProductSerializer(product) 
    #     return Response(serializer.data)
    # except  Product.DoesNotExist:
    #     return Response(status= status.HTTP_404_NOT_FOUND)
    


# Create your views here.
