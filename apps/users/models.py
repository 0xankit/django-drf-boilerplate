from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.manager import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom User Model

    Args:
        AbstractUser (AbstractUser): Django Abstract User Model
    """
    email = models.EmailField(verbose_name="email address",
                              max_length=255, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
