from django.contrib import admin
from parler.admin import TranslatableAdmin

from apps.models import Room, Course, Group


@admin.register(Room)
class RoomAdmin(TranslatableAdmin):
    list_display = ('name', 'capacity')


@admin.register(Course)
class CourseAdmin(TranslatableAdmin):
    list_display = ('name', 'price')


@admin.register(Group)
class GroupAdmin(TranslatableAdmin):
    list_display = ('name', 'teacher', 'time')
