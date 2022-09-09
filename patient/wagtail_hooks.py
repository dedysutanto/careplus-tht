from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView)
from .models import Patients, Soaps, NextAppointment
from crum import get_current_user
from config.utils import calculate_age
from django.core.exceptions import ObjectDoesNotExist


class PatientsEditView(EditView):
    page_title = 'Editing'

    def get_page_title(self):
        return 'Patient'

    def get_page_subtitle(self):
        try:
            next_v = NextAppointment.objects.get(patient=self.instance)
            return '{} ({}) - Next Visit: {}'.format(self.instance,
                                                     calculate_age(self.instance.dob),
                                                     next_v.datetime.strftime("%A %d %b %Y, %H:%M"))
        except ObjectDoesNotExist:
            return '%s (%d)' % (self.instance, calculate_age(self.instance.dob))


class SoapsEditView(EditView):
    page_title = 'Editing'

    def get_page_title(self):
        return 'SOAP'

    def get_page_subtitle(self):
        return '%s (%d)' % (self.instance.patient.name, calculate_age(self.instance.patient.dob))


class PatientsPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        if user.is_superuser:
            return False
        else:
            return True

    def user_can_delete_obj(self, user, obj):
        return False

    def user_can_edit_obj(self, user, obj):
        if user.is_superuser:
            return False
        else:
            return True


class SoapsPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        if user.is_superuser:
            return False
        else:
            return True

    def user_can_delete_obj(self, user, obj):
        return False

    def user_can_edit_obj(self, user, obj):
        if user.is_superuser:
            return False
        else:
            return True


class PatientsAdmin(ModelAdmin):
    model = Patients
    base_url_path = 'patients'  # customise the URL from default to admin/bookadmin
    menu_label = 'Patient'  # ditch this to use verbose_name_plural from model
    menu_icon = 'group'  # change as required
    menu_order = 50  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('number', 'name', 'gender', 'dob', 'calculate_age', 'phone', 'address', 'next_visit')
    search_fields = ('number', 'name', 'dob')
    permission_helper_class = PatientsPermissionHelper
    ordering = ['-number']
    #edit_template_name = 'patient/edit.html'
    edit_view_class = PatientsEditView

    def get_queryset(self, request):
        current_user = get_current_user()
        if not current_user.is_superuser:
            return Patients.objects.filter(user=current_user)
        else:
            return Patients.objects.all()


class SoapsAdmin(ModelAdmin):
    model = Soaps
    base_url_path = 'soaps'  # customise the URL from default to admin/bookadmin
    menu_label = 'SOAP'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ul'  # change as required
    menu_order = 60  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = (
        'number', 'doctor', 'patient', 'datetime', 'subjective', 'objective',
        'assessment', 'plan', 'additional_info',
    )
    list_filter = ('doctor',)
    search_fields = ('number', 'doctor', 'patient__name',)
    ordering = ['-number']
    permission_helper_class = SoapsPermissionHelper
    edit_view_class = SoapsEditView

    def get_queryset(self, request):
        current_user = get_current_user()
        if not current_user.is_superuser:
            return Soaps.objects.filter(user=current_user)
        else:
            return Soaps.objects.all()


modeladmin_register(PatientsAdmin)
modeladmin_register(SoapsAdmin)
