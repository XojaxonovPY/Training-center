from functools import wraps

from graphql import GraphQLError

from apps.models import User


def is_admin(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        user = info.context.user
        if user.role != User.RoleType.ADMIN:
            raise GraphQLError('You are not an admin')
        return func(self, info, *args, **kwargs)

    return wrapper


def is_teacher(func):
    @wraps(func)
    def wrapper(self, info, *args, **kwargs):
        user = info.context.user
        if user.role != User.RoleType.TEACHER:
            raise GraphQLError('You are not an teacher')
        return func(self, info, *args, **kwargs)

    return wrapper
