from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

class GroupPermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request,'user') and (request.user.is_authenticated):
            if (request.user.groups.filter(name="Buyer").exists() and not request.user.has_perm('accounts.can_view_buyer')):
                raise PermissionDenied('You do not have permission to view Buyer content')
            elif (request.user.groups.filter(name="Seller").exists() and not request.user.has_perm('accounts.can_view_seller')):
                raise PermissionDenied('You do not have permission to view Seller content')
        response = self.get_response(request)
        return response