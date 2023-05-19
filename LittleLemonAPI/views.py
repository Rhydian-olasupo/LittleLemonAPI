from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser,OR
from .serializers import CartSerializer,CategorySerializer,MenuItemSerializer,OrderItemSerializer,OrderSerializer,UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import status

from .permissions import IsMemberOfManagerGroup,IsMemberOfDeliveryGroup,IsACustomer

import datetime
from django.db.models import Sum 
from rest_framework.exceptions import PermissionDenied, ValidationError



class CategoriesView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsMemberOfManagerGroup|IsAdminUser|IsACustomer]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    #filter_backends = [SearchFilter]
    filterset_fields = ['price','featured','category']
    search_fields = ['title']

    '''def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        else:
            self.request.method == "POST"
            return [permissions.IsAuthenticated(),IsMemberOfManagerGroup()]'''



from django.http import Http404
class MenuItemSingle(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = MenuItemSerializer

    def get_object(self):
        try:
            return MenuItem.objects.get(id=self.kwargs['pk'])
        except MenuItem.DoesNotExist:
            raise Http404("MenuItem does not exist")
    
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        else:
            self.request.method != "POST"
            return [permissions.IsAuthenticated(),IsMemberOfManagerGroup()]



class CartItemsView(generics.ListCreateAPIView,generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsACustomer]
    serializer_class = CartSerializer
    lookup_field = 'item_id'
    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ManagerView(generics.ListCreateAPIView):
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMemberOfManagerGroup|IsAdminUser]
    def get(self, request):
        managers = Group.objects.get(name="Manager")
        managers_members = managers.user_set.all()
        serializer = UserSerializer(managers_members,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Get the Manager group object
        manager_group = Group.objects.get(name='Manager')
        # Get the user object from the request payload
        username = request.data.get('username')
        user = User.objects.get(username=username)
        # Assign the user to the Manager group
        user.groups.add(manager_group)
        # Return a 201-Created response
        return Response({"message":"user added to the manager group"},status=status.HTTP_201_CREATED)



class DeliveryView(generics.ListCreateAPIView):
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMemberOfManagerGroup|IsAdminUser]
    def get(self, request):
        delivery_crew = Group.objects.get(name="Delivery_crew")
        delivery_members = delivery_crew.user_set.all()
        serializer = UserSerializer(delivery_members,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Get the Delivery group object
        delivery_group = Group.objects.get(name='Delivery_crew')
        # Get the user object from the request payload
        username = request.data.get('username')
        user = User.objects.get(username=username)
        # Assign the user to the Delivery group
        user.groups.add(delivery_group)
        # Return a 201-Created response
        return Response({"message":"user added to the delivery group"},status=status.HTTP_201_CREATED)




class ManagerSingleView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMemberOfManagerGroup|IsAdminUser]
    serializer_class = UserSerializer

    def delete(self, request, userID):
        try:
            manager_group = Group.objects.get(name='Manager')
            user = User.objects.get(id=userID)
            if user in manager_group.user_set.all():
                manager_group.user_set.remove(user)
                return Response({"message": "User deleted from the Manager group."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is not in the Manager group."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class DeliverySingleView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMemberOfManagerGroup|IsAdminUser]
    serializer_class = UserSerializer

    def delete(self, request, userID):
        try:
            delivery_group = Group.objects.get(name='Delivery_crew')
            user = User.objects.get(id=userID)
            if user in delivery_group.user_set.all():
                delivery_group.user_set.remove(user)
                return Response({"message": "User deleted from the Delivery group."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is not in the Delivery group."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class OrderListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsACustomer|IsAdminUser|IsMemberOfManagerGroup]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery_crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        total = cart_items.aggregate(total=Sum('price'))['total']
        order = Order.objects.create(
            user=request.user,
            total=total,
            date=datetime.date.today()  # set date to today's date
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )

        cart_items.delete()

        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser|IsMemberOfManagerGroup|IsMemberOfDeliveryGroup]


    def get_queryset(self):
        return Order.objects.all()

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        delivery_crew_username = request.data.get('delivery_crew')
        delivery_crew_username = User.objects.get(username=delivery_crew_username)
        if delivery_crew_username:
            try:
                delivery_crew = User.objects.get(username=delivery_crew_username)
                if not delivery_crew.groups.filter(name ="Delivery_crew").exists():
                    raise ValidationError('This User is not a Delivery Member')

                instance.delivery_crew = delivery_crew_username
            except User.DoesNotExist:
                raise Http404("Invalid Username provided")
    
        # Update status field if it exists in request data
        status_value = request.data.get('status')
        if status_value is not None:
            # Check if a delivery crew is assigned before changing the status to 0 or 1
            if (delivery_crew is None and status_value in [0, 1]):
                raise ValidationError('Invalid combination of delivery_crew and status')
            instance.status = status_value
        # Allow delivery crew to update only the status field
        '''if instance.delivery_crew != request.user:
            raise PermissionDenied("You do not have permission to update this order")
        if status_value not in [0, 1]:
        raise ValidationError('Invalid status')
            instance.status = status_value
        else:
            raise PermissionDenied("You do not have permission to perform this action.")'''

        instance.save()
        serializer = self.get_serializer(instance, partial=partial)
        return Response(serializer.data)
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)