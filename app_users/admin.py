from django.contrib import admin
# from django.contrib.auth.models import Group
from . import models

# admin.site.unr(Group)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.ClassRoomTeacher)
admin.site.register(models.Class)
admin.site.register(models.Lesson)
admin.site.register(models.Homework)
admin.site.register(models.Attendance)
admin.site.register(models.Grade)
admin.site.register(models.ChatMessage)
admin.site.register(models.Parent)
