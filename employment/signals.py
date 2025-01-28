import os
from django.conf import settings
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from .models import Application, Employee, Employer, User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == 'employee':
            Employee.objects.create(user=instance)
        elif instance.account_type == 'employer':
            Employer.objects.create(user=instance)


@receiver(post_delete, sender=Application)
def delete_uploads(sender, instance: Application, **kwargs):
    if instance.resume:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.resume.name))
