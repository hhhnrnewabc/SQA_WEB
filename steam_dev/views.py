from django.shortcuts import render
from steam_dev.form import SteamDevForm, SteamDevAPPForm, SteamDevApplyForm
from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict


def index(request):
    return render(request, 'steam_dev/index.html')


def dev_apply(request):
    return render(request, 'steam_dev/dev_apply.html')


def get_steam_dev_or_signup_apply_http(user):
    if user.is_authenticated():
        steam_user, is_created = SteamUser.objects.get_or_create(baseuser=user)
    else:
        return None, HttpResponseRedirect(reverse('steam:user_signup'))
    try:
        steam_dev = SteamDeveloper.objects.get(baseuser=user, steam_user=steam_user)
    except SteamDeveloper.DoesNotExist:
            return None, HttpResponseRedirect(reverse('steam_dev:dev_apply'))
    return steam_dev, None


class SteamDevApplyView(FormView):
    template_name = 'steam_dev/dev_apply.html'
    success_url = 'dev_profile'
    form_class = SteamDevApplyForm
    _steam_user = None
    _steam_dev = None
    _user = None

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated():
            self._user = user
            self._steam_user, is_created = SteamUser.objects.get_or_create(baseuser=self._user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))

        self._steam_dev, is_created = SteamDeveloper.objects.get_or_create(baseuser=self._user,
                                                                           steam_user=self._steam_user)

        # load first/last name from steam_user
        if is_created:
            self._steam_dev.update({'first_name': self._steam_user.first_name, 'last_name': self._steam_user.last_name})
            self._steam_dev.save()

        return super(SteamDevApplyView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            self._steam_dev, http = get_steam_dev_or_signup_apply_http(user)
            if self._steam_dev:
                return HttpResponseRedirect(reverse('steam_dev:dev_profile'))
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))
        return super(SteamDevApplyView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        return super(SteamDevApplyView, self).get_initial()



class SteamDevView(FormView):
    template_name = 'steam_dev/dev_profile.html'
    form_class = SteamDevForm
    success_url = 'dev_profile'
    _steam_user = None
    _steam_dev = None
    _user = None

    def form_valid(self, form):

        return super(SteamDevView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        self._steam_dev, http = get_steam_dev_or_signup_apply_http(user)
        if http:
            return http
        return super(SteamDevView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # load data
        return model_to_dict(self._steam_dev)


class SteamDevAPPView(FormView):
    template_name = 'steam_dev/dev_app.html'
    form_class = SteamDevAPPForm
    success_url = 'dev_app'
    _steam_dev = None

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        self._steam_dev, http = get_steam_dev_or_signup_apply_http(user)
        if http:
            return http
        return super(SteamDevAPPView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # load data
        return model_to_dict(self._steam_dev)


class SteamDevCreateView(FormView):
    template_name = 'steam_dev/dev_profile.html'
    form_class = SteamDevForm
    success_url = 'dev_profile'
    _is_created = None
    _steam_user = None
    _steam_dev = None
    _user = None

    def form_valid(self, form):

        return super(SteamDevCreateView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            self._user = user
            self._steam_user, is_created = SteamUser.objects.get_or_create(baseuser=self._user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))

        self._steam_dev, self._is_created = SteamDeveloper.objects.get_or_create(baseuser=self._user,
                                                                                 steam_user=self._steam_user)
        if not self._is_created:
            return HttpResponseRedirect(reverse('steam_dev:dev_profile'))

        return super(SteamDevCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # load data
        return model_to_dict(self._steam_dev)

