from rest_framework import permissions

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user

        if request.method in ['POST', 'PATCH', 'DELETE']:
            return request.user.is_authenticated
