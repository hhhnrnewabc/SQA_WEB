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
from django.conf import settings
from django.views.decorators.debug import sensitive_post_parameters
import datetime
# from steam.form import (GameForm_1_Name, GameForm_2_Version,
#                           GameForm_3_Language, GameForm_4_SysRequirement,
#                           GameForm_5_UpdatedDate, GameReviewsForm)


def index(request):
    return render(request, 'steam/index.html')


def game_index(request):
    return render(request, 'steam/game_index.html')


def login_page(request):
    return render(request, 'steam/login.html', )


@sensitive_post_parameters('password')
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
            messages.success(request, _('Login Success'))
            if next == "":
                return HttpResponseRedirect(reverse('steam:index'))
            else:
                return HttpResponseRedirect(next)

        else:
            # Return a 'disabled account' error message
            messages.error(request, _('Disabled account'))
            return render_to_response('steam/login.html',
                                      context_instance=RequestContext(request))

    else:
        # Return an 'invalid login' error message.
        messages.error(request, _('Invalid login'))
        return render_to_response('steam/login.html', {'user_email': email},
                                  context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    messages.success(request, _('Logout Success'))
    return HttpResponseRedirect(reverse('steam:index'))


def resend_email(request):
    can_send_mail_time = True
    send_mail_time = request.session.get('_send_signup_mail_time', None)
    if send_mail_time:
        send_mail_time = datetime.datetime.fromtimestamp(send_mail_time)
    if not send_mail_time or send_mail_time + datetime.timedelta(minutes=10) > datetime.datetime.now():
        can_send_mail_time = False
    return render_to_response('steam/resend_email.html', {'can_send_mail_time': can_send_mail_time, },
                              context_instance=RequestContext(request))


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
            return HttpResponse('{"status":"error"}', mimetype='application/json')

        if user.is_active:
            return HttpResponse('{"status": "is_already_active"}', mimetype='application/json')
        send_mail_time = self.request.session.get('_send_signup_mail_time', None)
        if send_mail_time:
            send_mail_time = datetime.datetime.fromtimestamp(send_mail_time)
            if send_mail_time + datetime.timedelta(minutes=10) > datetime.datetime.now():
                return HttpResponse('{"status":"please wait 10 minutes."}', mimetype='application/json')

        self.request.session["_send_signup_mail_time"] = datetime.datetime.now().timestamp()
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
        return HttpResponse('{"status":"ok"}', mimetype='application/json')


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
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'current_app': None,
            'extra_context': None,
            'html_email_template_name': None
    }
    return password_reset(request, **c)


# def game_edit(request):
#     mode = request.session.get('edit_mode', None)
#     edit_step = request.session.get('editing_game_step', None)
#     game_id = request.session.get('editibg_game_is', None)

#     if edit_step:
#         form_dict = {'1': GameForm_1_Name(),
#                      '2': GameForm_2_Version(),
#                      '3': GameForm_3_Language(),
#                      '4': GameForm_4_SysRequirement(),
#                      '5': GameForm_5_UpdatedDate()}

#         form = form_dict.get('edit_step', None)

#         if request.POST:
#             if mode and game_id:
#                 game = Game.objects.get(id=game_id)
#                 form = form(request.POST, instance=game)
#             else:
#                 form = form(request.POST)

#             if form.is_valid():
#                 form.save()
#                 if int(edit_step) <=5:
#                 request.session['editing_game_step'] = str(int(edit_step)+1)
#                 return HttpResponseRedirect



