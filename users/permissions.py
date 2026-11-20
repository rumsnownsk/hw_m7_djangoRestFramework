#permissions.py
from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """ Проверяет, является ли пользователь Модератором."""
    message = 'some text'

    def has_permission(self, request, view):
        # print("METHOD:", request.method, "PERMS:", view.permission_classes)
        return request.user.groups.filter(name='moders').exists()

class NotModer(permissions.BasePermission):
    """Запрещает действие модераторам."""
    message = "Модераторы не могут выполнять это действие."

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = "Действие доступно только владельцу."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

