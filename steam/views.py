from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
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
            steam_user = get_object_or_404(SteamUser, baseuser=user)
            if steam_user:
                steam_user.create_new_secret_token()
            # Redirect to a success page.
            if next == "":
                return HttpResponseRedirect(reverse('steam:index'))
            else:
                return HttpResponseRedirect(next)

        else:
            # Return a 'disabled account' error message
            return render_to_response('steam/login.html', {'login_faill': _("disabled account"), },
                context_instance=RequestContext(request))

    else:
        # Return an 'invalid login' error message.
        return render_to_response('steam/login.html',
                                  {'login_faill': _("invalid login"), }, context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return render_to_response('steam/index.html', {'logout_success': _("Logout Success"), },
                              context_instance=RequestContext(request, ))


class CreateUserView(FormView):
    template_name = 'steam/create_user.html'
    form_class = UserCreationForm
    success_url = 'thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        #Get user email
        self.request.session['user'] = form.save().get_short_name()
        return super(CreateUserView, self).form_valid(form)


class ThanksView(generic.View):

    def get(self, request, *args, **kwargs):

        text = '<div class="redirect">'
        text += request.session['user']
        text += _(' is not active. Please check the URL.  Otherwise, '
                '<a href="/steam/active_user/"> here</a> '
                'to active ')
        text += '</div>'
        return HttpResponse(text)


def active_user(request):
    email = request.session.get('user', None)
    user = get_object_or_404(BaseUser, email=email)
    if user:
        user.is_active = True
        user.save()

        #AUTOMATIC LOGIN
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)

    return render_to_response('steam/index.html', {'signup_success': _("Sign up Success"), },
                              context_instance=RequestContext(request, ))



