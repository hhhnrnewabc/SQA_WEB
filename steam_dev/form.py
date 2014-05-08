from django import forms
from steam_dev.models import SteamDeveloper
from django.utils.translation import ugettext_lazy as _


class CreateSteamDevForm(forms.ModelForm):

    class Meta:
        model = SteamDeveloper
        fields = ('baseuser', 'steam_user', 'first_name', 'last_name', 'address', 'work_phone', 'fax', 'office_name',)

    def __init__(self, *args, **kwargs):
        super(CreateSteamDevForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        steam_use = super(CreateSteamDevForm, self).save(commit=False)
        if commit:
            steam_use.save()
        return steam_use




