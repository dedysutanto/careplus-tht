from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper)
from .models import Doctors
from crum import get_current_user


class DoctorsPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        if user.is_superuser:
            return False
        else:
            if Doctors.objects.count() >= 3:
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


class DoctorsAdmin(ModelAdmin):
    model = Doctors
    base_url_path = 'doctors'  # customise the URL from default to admin/bookadmin
    menu_label = 'Doctor'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    menu_order = 30  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ('name', 'phone', 'email', 'address')
    permission_helper_class = DoctorsPermissionHelper
    search_fields = ('name',)

    def get_queryset(self, request):
        current_user = get_current_user()
        if not current_user.is_superuser:
            return Doctors.objects.filter(user=current_user)
        else:
            return Doctors.objects.all()


modeladmin_register(DoctorsAdmin)
