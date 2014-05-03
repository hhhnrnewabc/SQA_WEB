from django import forms
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from django.utils.safestring import mark_safe


class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<div class="thumbnail album-pic"> <a target="_blank" href="%s">'
                           '<img src="%s"  data-src="holder.js/300x300" \
                           alt="300x300" /></a> </div>'
                           % (value.url, value.url)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'required': True}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'required': True}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = BaseUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = BaseUser.objects.create_user(email=self.cleaned_data['email'],
                                            password=self.cleaned_data["password1"])
        # user = super(UserCreationForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



