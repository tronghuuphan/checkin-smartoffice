from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Manager

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_manager_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Manager.objects.create(user=kwargs['instance'])