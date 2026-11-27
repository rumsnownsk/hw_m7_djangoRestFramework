# permissions.py
from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь Модератором."""

    message = "some text"

    def has_permission(self, request, view):
        # print("METHOD:", request.method, "PERMS:", view.permission_classes)
        return request.user.groups.filter(name="moders").exists()


class NotModer(permissions.BasePermission):
    """Запрещает действие модераторам."""

    message = "Модераторы не могут выполнять это действие."

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    message = "Вы можете управлять только своим профилем."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsCurrentUser(permissions.BasePermission):
    message = "Вы можете управлять только своим профилем."

    # has_object_permission: проверка конкретного объекта
    def has_object_permission(self, request, view, obj):
        # obj — это тот User, которого DRF нашёл по pk в URL
        # request.user — тот, кто делает запрос
        return obj.id == request.user.id
        # или проще: return obj == request.user
