from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

class GroupPermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request,'user') and (request.user.is_authenticated) and (not request.user.is_superuser):
            if (not request.user.groups.filter(name="Buyer").exists()):
                raise PermissionDenied('You do not have permission to view or edit Buyer content')
            elif (not request.user.groups.filter(name="Seller").exists()):
                raise PermissionDenied('You dont have permission to view or edit Seller content')
        response = self.get_response(request)
        return response