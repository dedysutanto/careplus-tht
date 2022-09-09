from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class MemberStatus(models.Model):
    name = models.CharField(max_length=30)
    is_clinic = models.BooleanField(default=False)

    class Meta:
        db_table = 'member_status'
        verbose_name = 'Member Status'
        verbose_name_plural = 'Member Status'

    def __str__(self):
        return '%s' % self.name


class User(AbstractUser):
    clinic_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    membership = models.ForeignKey(
        MemberStatus,
        on_delete=models.CASCADE,
        verbose_name=_('Membership'),
        null=True,
        blank=True
    )
