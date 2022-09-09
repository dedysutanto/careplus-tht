from django import forms
from wagtail.users.forms import UserEditForm, UserCreationForm
from wagtail.users.models import UserProfile
from wagtail.admin.forms.account import NameEmailForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import MemberStatus


class CustomUserEditForm(UserEditForm):
    phone = forms.TextInput
    address = forms.Textarea
    membership = forms.ModelChoiceField(queryset=MemberStatus.objects,
                                        required=True,
                                        disabled=True,
                                        label=_("Membership"))


class CustomUserCreationForm(UserCreationForm):
    phone = forms.TextInput
    address = forms.Textarea
    membership = forms.ModelChoiceField(queryset=MemberStatus.objects,
                                        required=True,
                                        label=_("Membership"))


class ClinicFieldsSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['clinic_name']


class AdditionalFieldsSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['phone', 'address']


'''
class CustomProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #fields = ['first_name', 'last_name']
        fields = ['phone', 'address']
'''

'''
User = get_user_model()


class NewNameEmailForm(NameEmailForm):
    #first_name = forms.CharField(required=True, label=_("First Name"))
    #last_name = forms.CharField(required=True, label=_("Last Name"))
    name = forms.CharField(required=True, label=_("Clinic/Doctor Name"))
    email = forms.EmailField(required=True, label=_("Email"))

    def __init__(self, *args, **kwargs):
        from wagtail.admin.views.account import email_management_enabled

        super().__init__(*args, **kwargs)

        if not email_management_enabled():
            del self.fields["email"]

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super().clean()
        self.first_name = cleaned_data.get('name')
        self.last_name = cleaned_data.get('name')
        self.name = cleaned_data.get('name')
'''