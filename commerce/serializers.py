from rest_framework import serializers 
from django.core.validators import MinValueValidator

from .models import (
    Product,
    Address,
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    User
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'birth_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message='The price must be greater than 0.0')])
    stock = serializers.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = Product
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at', ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', ]


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message='The total must be greater than 0.0')])

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(validators=[MinValueValidator(0)])
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message='The price must be greater than 0.01')])

    class Meta:
        model = OrderItem
        fields = '__all__'