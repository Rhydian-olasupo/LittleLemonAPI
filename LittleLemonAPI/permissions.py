from rest_framework.permissions import BasePermission

class IsMemberOfManagerGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsMemberOfDeliveryGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()
    
class IsACustomer(BasePermission):
    def has_permission(self, request, view):
        excluded_groups = ['Manager', 'Delivery Crew']
        return not request.user.groups.filter(name__in =excluded_groups).exists()
    