from django.contrib import admin
from .models import MenuItem,Cart,Order,OrderItem,Category

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)