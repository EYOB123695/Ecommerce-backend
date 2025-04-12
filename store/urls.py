from django.urls import path 
from django.urls import include
from . import views 
from rest_framework_nested import routers 
from rest_framework.routers import DefaultRouter, SimpleRouter
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register("carts" , views.CartViewSet, basename='carts')
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
carts_router =  routers.NestedDefaultRouter(router , "carts" , lookup = 'cart')
carts_router.register("items" , views.CartItemViewSet , basename = "cart-items")
urlpatterns = router.urls + product_router.urls + carts_router.urls

 
# urlpatterns = [  
#     path('products/' , views.ProductList.as_view()), 
#     path('products/<int:id>/' , views.ProductDetail.as_view()),
# ]