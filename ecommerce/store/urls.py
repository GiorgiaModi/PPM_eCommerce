from django.urls import path
from . import views
from .views import *
#from .views import add_to_cart

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    #path('add_to_cart/<int:pk>/', add_to_cart, name="add_to_cart"),
]