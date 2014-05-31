from django import forms
from django.conf import settings
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


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
    email = forms.EmailField(label=_('Email'),
                             error_messages={'unique': _("This email has already been registered."),
                                             'invalid': _("This is not the e-mail format")},
                             widget=forms.EmailInput(attrs={'required': True}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'required': True,
                                'data-toggle': 'tooltip', 'data-trigger': 'manual', 'data-title': _("Caps lock is on")}))
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput(attrs={'required': True,
                                'data-toggle': 'tooltip', 'data-trigger': 'manual', 'data-title': _("Caps lock is on")}))

    class Meta:
        model = BaseUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
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


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=settings.EMAIL_HOST_USER, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import EmailMessage
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            msg = EmailMessage(subject, email, from_email, [user.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
