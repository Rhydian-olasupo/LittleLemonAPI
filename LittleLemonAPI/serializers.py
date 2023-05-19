from .models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    #category_id = serializers.IntegerField(write_only = True)
    #category = CategorySerializer(read_only = True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source = 'user', queryset=User.objects.all(), 
    default=serializers.CurrentUserDefault() 
    ) 
    menuitem = MenuItem()
    class Meta:
        model = Cart
        fields = ['id','quantity','unit_price','price','user_id','menuitem']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'delivery_crew', 'status', 'total', 'date', 'order_items']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}