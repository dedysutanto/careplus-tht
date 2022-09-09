from django.db import models
#from django.contrib.auth.models import User
from account.models import User
from crum import get_current_user
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel


class Doctors(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    phone = models.CharField(_('Telephone/HP'), max_length=50)
    email = models.EmailField(_('Email'), blank=True, null=True)
    address = models.TextField(_('Address'), blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldPanel('name'),
        FieldRowPanel([FieldPanel('phone'), FieldPanel('email')]),
        FieldPanel('address')

    ]

    class Meta:
        db_table = 'doctor'
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            self.user = get_current_user()

        #self.name = self.name.upper()
        self.email = str(self.email).lower()
        #self.address = self.address.upper()

        return super(Doctors, self).save()
