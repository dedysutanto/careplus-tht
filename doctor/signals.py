from doctor.models import Doctors
from account.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
def create_doctor(sender, instance, created, **kwargs):
    if created:
        try:
            instance.membership.is_clinic
            if not instance.membership.is_clinic:
                doctor = Doctors()
                doctor.name = instance.first_name + ' ' + instance.last_name
                doctor.email = instance.email
                doctor.phone = instance.phone
                doctor.address = instance.address
                doctor.user = instance
                doctor.save()
        except AttributeError:
            pass

    else:
        try:
            instance.membership.is_clinic
            if not instance.membership.is_clinic:
                try:
                    doctor = Doctors.objects.get(user=instance)
                    doctor.name = instance.first_name + ' ' + instance.last_name
                    doctor.email = instance.email
                    doctor.phone = instance.phone
                    doctor.address = instance.address
                    doctor.user = instance
                    doctor.save()
                except ObjectDoesNotExist:
                    pass
        except AttributeError:
            pass


@receiver(post_delete, sender=User)
def delete_doctor(sender, instance, **kwargs):
    try:
        instance.membership.is_clinic
        if not instance.membership.is_clinic:
            try:
                Doctors.objects.get(user=instance).delete()
            except ObjectDoesNotExist:
                pass
    except AttributeError:
        pass
