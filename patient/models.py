from django.db import models
from doctor.models import Doctors
#from django.contrib.auth.models import User
from account.models import User
from modelcluster.models import ClusterableModel
from django.utils.translation import gettext_lazy as _
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from django.utils.timezone import now
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, HelpPanel
from crum import get_current_user
from wagtail.admin import widgets
from config.utils import calculate_age
from django.core.exceptions import ObjectDoesNotExist


GENDER = [
    ('M', 'Male'),
    ('F', 'Female')
]


class Patients(ClusterableModel):
    number = models.CharField(_('ID'), max_length=16, unique=True)
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    gender = models.CharField(max_length=3, verbose_name=_('Gender'), choices=GENDER, default='M')
    dob = models.DateField(verbose_name=_('Date of Birth'))
    address = models.TextField(verbose_name=_('Address'), blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name=_('Telephone/HP'), blank=True, null=True)
    email = models.EmailField(_('Email'), blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    date_widget = widgets.AdminDateInput(
        attrs={
            'placeholder': 'yyyy-mm-dd'
        }
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('name'), FieldPanel('gender')]),
            FieldPanel('dob', widget=date_widget),
            FieldRowPanel([FieldPanel('phone'), FieldPanel('email')]),
            FieldPanel('address')],
            heading='Data Patient'
        ),
        InlinePanel('related_patient', heading="Related SOAP", label='Detail SOAP',
                    classname="collapsed"),

        InlinePanel('next_appointment', heading="Next Visit", label='Date Time',
                    min_num=0, max_num=1),

    ]

    class Meta:
        db_table = 'patients'
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    def __str__(self):
        return '%s' % self.name

    def save(self):
        if self.user is None:
            self.user = get_current_user()

        self.name = self.name.upper()
        self.address = self.address.upper()

        if len(str(self.number)) != 16:
            number = Patients.objects.filter(user=self.user).count() + 1
            prefix = 'MR{:04d}'.format(self.user.id)
            self.number = '{}{:010d}'.format(prefix, number)
            print('Medical Record', self.number)

        '''
        try:
            self.number
            print('Number Exist', self.number)

            if 'MR1' not in self.number:
                self.number = 'MR1' + self.number
        except ObjectDoesNotExist:
            print('Number', self.number)
            number = Patients.objects.count() + 1
            self.number = 'MR1{:08d}'.format(number)
        '''

        return super(Patients, self).save()

    def calculate_age(self):
        '''

        today = date.today()
        try:
            age = (today.year - self.dob.year) \
                  - ((today.month, today.day) < (self.dob.month, self.dob.day))
        except ValueError:
            age = 0
        #return '%d' % age
        '''
        return '%d' % calculate_age(self.dob)

    calculate_age.short_description = _('Age')

    def next_visit(self):
        try:
            next_v = NextAppointment.objects.get(patient=self)
            from datetime import datetime
            return '%s' % next_v.datetime.strftime("%A %d %b %Y, %H:%M")

        except ObjectDoesNotExist:
            return '%s' % _('No appointment')

    next_visit.short_description = _('Next Visit')


class Soaps(Orderable):
    def limit_choices_to_current_user():
        user = get_current_user()
        if not user.is_superuser:
            return {'user': user}
        else:
            return {}

    number = models.CharField(_('ID'), max_length=16, unique=True)
    doctor = models.ForeignKey(
        Doctors,
        on_delete=models.RESTRICT,
        verbose_name=_('Doctor'),
        limit_choices_to=limit_choices_to_current_user,
    )
    datetime = models.DateTimeField(_('Date Time'), default=now)
    subjective = models.TextField(_('Subjective'))
    objective = models.TextField(_('Objective'))
    assessment = models.TextField(_('Assessment'))
    plan = models.TextField(_('Plan'))

    additional_info = models.TextField(verbose_name=_('Additional Information'), blank=True, null=True)
    patient = ParentalKey(
        'Patients',
        on_delete=models.CASCADE,
        related_name='related_patient',
        limit_choices_to=limit_choices_to_current_user,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    image = models.ImageField(upload_to='soap/images', blank=True, null=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [
        FieldRowPanel([FieldPanel('doctor'), FieldPanel('patient'), FieldPanel('datetime')]),
        MultiFieldPanel([
            FieldPanel('subjective'),
            FieldPanel('objective'),
            FieldPanel('assessment'),
            FieldPanel('plan'),
        ], heading='SOAP'),
        FieldPanel('additional_info'),
        FieldPanel('image'),
    ]

    class Meta:
        db_table = 'soaps'
        verbose_name = 'SOAP'
        verbose_name_plural = 'SOAP'
        ordering = ['-datetime']

    def save(self):
        if self.user is None:
            self.user = get_current_user()

        if len(str(self.number)) != 16:
            number = Soaps.objects.filter(user=self.user, doctor=self.doctor, patient=self.patient).count() + 1
            prefix = 'SOAP{:04d}{:02d}{:03}'.format(self.user.id, self.doctor.id, self.patient.id)
            self.number = '{}{:03d}'.format(prefix, number)
            print('SOAP', self.number)
        return super(Soaps, self).save()


class NextAppointment(Orderable):
    datetime = models.DateTimeField(_('Date Time'), null=True, blank=True)
    patient = ParentalKey('Patients', on_delete=models.CASCADE, related_name='next_appointment')

    panels = [FieldPanel('datetime')]

    class Meta:
        db_table = 'next_appointment'

'''
class MedicalImage(Orderable):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    patient = ParentalKey('Patients', on_delete=models.CASCADE, related_name='medical_image')

    panels = [
        FieldPanel('image'),
    ]

    class Meta:
        db_table = 'medical_image'
'''
