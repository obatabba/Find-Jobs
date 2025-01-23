from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Employee, Employer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == 'employee':
            Employee.objects.create(user=instance)
        elif instance.account_type == 'employer':
            Employer.objects.create(user=instance)