from django import forms
from steam_dev.models import SteamUser



class CreateSteamDevForm(forms.ModelForm):

    class Meta:
        model = SteamUser
        fields = ('baseuser', 'steam_user', )

    def __init__(self, *args, **kwargs):
        super(CreateSteamDevForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        steam_use = super(CreateSteamDevForm, self).save(commit=False)
        if commit:
            steam_use.save()
        return steam_use




