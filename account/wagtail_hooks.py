from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.admin.views.account import BaseSettingsPanel
from wagtail import hooks
from .forms import AdditionalFieldsSettingsForm, ClinicFieldsSettingsForm
from .models import MemberStatus


@hooks.register('construct_main_menu')
def hide_doctor_menu_item(request, menu_items):
    try:
        request.user.membership.is_clinic
        if not request.user.membership.is_clinic:
            menu_items[:] = [item for item in menu_items if item.name != 'doctor']
    except AttributeError:
        pass


class ClinicSettingsPanel(BaseSettingsPanel):
    name = 'custom'
    title = 'Clinic Name'
    order = 000
    form_class = ClinicFieldsSettingsForm
    form_object = 'user'
    #template_name = 'account/admin/clinic_settings.html'


@hooks.register('register_account_settings_panel', order=1)
def register_custom_settings_panel(request, user, profile):
    if user.is_superuser:
        return None
    else:
        try:
            user.membership.is_clinic
            if user.membership.is_clinic:
                return ClinicSettingsPanel(request, user, profile)
            else:
                return None
        except AttributeError:
            pass


@hooks.register('register_account_settings_panel', order=2)
class AdditionalFieldsSettingsPanel(BaseSettingsPanel):
    name = 'custom'
    title = 'Phone and Address'
    order = 200
    form_class = AdditionalFieldsSettingsForm
    form_object = 'user'


class MemberStatusAdmin(ModelAdmin):
    model = MemberStatus
    base_url_path = 'memberstatus'  # customise the URL from default to admin/bookadmin
    menu_label = 'Membership'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pick'  # change as required
    menu_order = 10  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'is_clinic',)
    search_fields = ('name',)


modeladmin_register(MemberStatusAdmin)
