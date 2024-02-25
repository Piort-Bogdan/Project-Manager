from rest_framework import permissions


class IsAuthenticateAndAccountOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the owner of the account
        return request.user == obj
