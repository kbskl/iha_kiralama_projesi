from rest_framework import permissions

"""
Açıklama:
Rest Framework'te view içlerinde kontrol yapmak yerine burada daha genel ve kullanışlı özel permissionlar tanımlanmıştır.
"""


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
