from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_doctor(sender, instance, created, **kwargs):
    if created:
        instance.clinic_name = '{} {}'.format(instance.first_name, instance.last_name)
        instance.save()
