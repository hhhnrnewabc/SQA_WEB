from django import forms
from steam_user.models import SteamUser
from steam.form import AdminImageWidget
from django.utils.translation import ugettext_lazy as _


class SteamUserForm(forms.ModelForm):
    photo = forms.ImageField(_('Image'), label=_('Image'), help_text=_('Image:jpg'), widget=AdminImageWidget)

    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'cell_phone', 'sex', 'photo', )

    def __init__(self, *args, **kwargs):
        super(SteamUserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        steam_use = super(SteamUserForm, self).save(commit=False)
        if commit:
            steam_use.save()
        return steam_use

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            try:
                if photo._size > 1*1024*1024:
                    raise forms.ValidationError("Image file too large ( > 1mb )")

            # no new upload image return old image
            except AttributeError:
                return self.instance.photo

            # return new upload image
            return photo
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
