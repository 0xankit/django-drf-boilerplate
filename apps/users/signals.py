from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        print(f'New user created: {instance.username}')
