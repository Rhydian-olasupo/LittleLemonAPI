from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[
    path('category', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.MenuItemSingle.as_view()),
    path('cart/menu-items',views.CartItemsView.as_view()),
    #path('orders',views.OrdersView.as_view()),
    path('groups/manager/users',views.ManagerView.as_view()),
    path('groups/delivery-crew/users',views.DeliveryView.as_view()),
    path('groups/manager/users/<int:userID>', views.ManagerSingleView.as_view()),
    path('groups/delivery-crew/users/<int:userID>', views.DeliverySingleView.as_view()),
    path('orders',views.OrderListCreateView.as_view()),
    path('orders/<int:id>', views.OrderDetailView.as_view()),

    #path('ratings', views.RatingsView.as_view()),
    ]