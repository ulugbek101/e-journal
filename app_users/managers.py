from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class StudentManager(models.Manager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type='STUDENT')
        return queryset


class TeacherManager(models.Manager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type='TEACHER')
        return queryset


class ClassRoomTeacherManager(models.Manager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type='CLASS_ROOM_TEACHER')
        return queryset


class ParentManager(models.Manager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type='PARENT')
        return queryset
