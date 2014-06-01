from django import forms
from steam.form import AdminImageWidget
from steam_dev.models import SteamDeveloper, SteamDevAPPS
from django.utils.translation import ugettext_lazy as _


def _get_cleaner(form, field):
    def clean_field():
        return getattr(form.instance, field, None)
    return clean_field


class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.items() if name in self.readonly_fields):
            field.widget.attrs['readonly'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        for field in self.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class SteamDevForm(ReadOnlyFieldsMixin, forms.ModelForm):

    class Meta:
        model = SteamDeveloper
        fields = ('first_name', 'last_name', 'work_phone', 'fax',
                  'company_name', 'address')

    def __init__(self, *args, **kwargs):
        super(SteamDevForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        steam_dev = super(SteamDevForm, self).save(commit=False)
        if commit:
            steam_dev.save()
        return steam_dev


class SteamDevAppApiTokenView(forms.ModelForm):

    readonly_fields = ('api_token', 'secret_token',)

    class Meta:
        model = SteamDevAPPS
        fields = ('app_name',)


class SteamDevAPPForm(forms.ModelForm):

    class Meta:
        model = SteamDevAPPS
        fields = ('web_url', 'app_name', 'app_introduction', 'photo_big', 'photo_small',)
        readonly_fields = ('api_token', 'secret_token', 'created',)

    def __init__(self, *args, **kwargs):
        super(SteamDevAPPForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        steam_dev_app = super(SteamDevAPPForm, self).save(commit=False)
        if commit:
            steam_dev_app.save()
        return steam_dev_app


class SteamDevApplyForm(forms.Form):

    agree = forms.BooleanField(_('I Agree'), label=_('I Agree'), widget=forms.CheckboxInput,
                               error_messages={'required': 'You must agree to the terms and conditions to continue'},
                               help_text=_('If you agree the terns. Please check I agree.'))
