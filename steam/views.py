from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from steam.models import Game
from django.forms.models import model_to_dict
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from steam.form import UserCreationForm
from django.views.generic.edit import FormView
from django.views import generic
from django.http import Http404
from django.contrib import messages
from django.utils.translation import ugettext as _
from baseuser.tokens import signup_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.models import get_current_site
from django.template import loader


def index(request):
    return render(request, 'steam/index.html')


def login_page(request):
    return render(request, 'steam/login.html', )


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('steam:index', ))

    email = request.POST.get('Email', '')
    password = request.POST.get('UserPassword', '')
    next = ""

    if request.GET:
        next = request.GET['next']

    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            steam_user, is_create = SteamUser.objects.get_or_create(baseuser=user)
            if not is_create:
                steam_user.create_new_secret_token()
            # Redirect to a success page.
            if next == "":
                return HttpResponseRedirect(reverse('steam:index'))
            else:
                return HttpResponseRedirect(next)

        else:
            # Return a 'disabled account' error message
            return render_to_response('steam/login.html', {'login_fall': _("disabled account"), },
                context_instance=RequestContext(request))

    else:
        # Return an 'invalid login' error message.
        return render_to_response('steam/login.html',
                                  {'login_fall': _("invalid login"),
                                   'user_email': email
                                   }, context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return render_to_response('steam/index.html', {'logout_success': _("Logout Success"), },
                              context_instance=RequestContext(request, ))


class CreateUserView(FormView):
    template_name = 'steam/create_user.html'
    form_class = UserCreationForm
    success_url = 'thanks/'
    use_https = True

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.session["_auth_user_id"] = form.save().id
        messages.success(self.request, _("Create User Success"))
        return super(CreateUserView, self).form_valid(form)


class ThanksView(generic.TemplateView):
    template_name = 'steam/signup_thanks.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('steam:index', ))
        return super(ThanksView, self).dispatch(request, *args, **kwargs)


class EmailView(generic.View):

    def get(self, request, *args, **kwargs):
        try:
            user = BaseUser.objects.get(id=self.request.session["_auth_user_id"])
        except (BaseUser.DoesNotExist, TypeError, ValueError, OverflowError, KeyError):
            return HttpResponse("{'status':'error'}")

        if user.is_active:
            return HttpResponse("{'status': 'is_already_active'}")
        token = signup_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = self.request.is_secure()
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token,
            'protocol': 'https' if use_https else 'http',
        }
        subject = loader.render_to_string('steam/email_confirm.html', c)
        user.email_user(_('Welcome SQA Game Center Project'), subject)
        return HttpResponse("{'status':'ok'}")


def active_user(request, uidb64, token):
    if token:
        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = user_model._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and user.is_active:
            return HttpResponseRedirect(reverse('steam:index'))

        if user is not None and signup_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            #AUTOMATIC LOGIN
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

            return render_to_response('steam/index.html', {'signup_success': _("Sign up Success"), },
                                  context_instance=RequestContext(request, ))

    return HttpResponse(status=404)


from django.contrib.auth.views import (password_reset, password_reset_done,
                                       password_reset_confirm, password_reset_complete)
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from baseuser.tokens import default_token_generator


def baseuser_password_reset(request):
    c = {
            'is_admin_site': False,
            'template_name': 'steam/password_reset_form.html',
            'email_template_name': 'steam/password_reset_email.html',
            'subject_template_name': 'steam/password_reset_subject.txt',
            'password_reset_form': PasswordResetForm,
            'token_generator': default_token_generator,
            'post_reset_redirect': None,
            'from_email': None,
            'current_app': None,
            'extra_context': None,
            'html_email_template_name': None
    }
    return password_reset(request, **c)