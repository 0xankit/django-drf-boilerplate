from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.manager import CustomUserManager


class Role(models.Model):
    """
    Role Model for User Role

    Args:
        models (Model): Django Model

    Returns:
        str: Role Name
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class Designation(models.Model):
    """
    Designation Model for User Designation

    Args:
        models (Model): Django Model
    Returns:
        str: Designation Title
    """
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.title)


class CustomUser(AbstractUser):
    """
    Custom User Model

    Args:
        AbstractUser (AbstractUser): Django Abstract User Model
    """
    email = models.EmailField(verbose_name="email address",
                              max_length=255, unique=True)
    roles = models.ManyToManyField(
        Role, related_name='users')
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
