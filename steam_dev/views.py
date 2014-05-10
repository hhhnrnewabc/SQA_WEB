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


# require for steam_dev
# if get steam_dev will set to _steam_dev
# Class must have _steam_dev
def steam_dev_required(function):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            steam_user, is_created = SteamUser.objects.get_or_create(baseuser=user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))
        try:
            steam_dev = SteamDeveloper.objects.get(baseuser=user, steam_user=steam_user)
        except SteamDeveloper.DoesNotExist:
            return HttpResponseRedirect(reverse('steam_dev:dev_apply'))
        self._steam_dev = steam_dev
        return function(self, request, *args, **kwargs)
    return dispatch


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

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            self._user = user
            self._steam_user, is_created = SteamUser.objects.get_or_create(baseuser=self._user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))

        try:
            self._steam_dev = SteamDeveloper.objects.get(baseuser=self._user, steam_user=self._steam_user)
        except SteamDeveloper.DoesNotExist:
            pass
        else:
            return HttpResponseRedirect(reverse('steam_dev:dev_profile'))
        return super(SteamDevApplyView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return super(SteamDevApplyView, self).get_initial()


class SteamDevView(FormView):
    template_name = 'steam_dev/dev_profile.html'
    form_class = SteamDevForm
    success_url = 'dev_profile'
    _steam_dev = None
    _user = None

    def form_valid(self, form):

        return super(SteamDevView, self).form_valid(form)

    @steam_dev_required
    def dispatch(self, request, *args, **kwargs):
        return super(SteamDevView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        # load data
        return model_to_dict(self._steam_dev)


class SteamDevAPPView(FormView):
    template_name = 'steam_dev/dev_app.html'
    form_class = SteamDevAPPForm
    success_url = 'dev_app'
    _steam_dev = None

    @steam_dev_required
    def dispatch(self, request, *args, **kwargs):
        return super(SteamDevAPPView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        # load data
        return model_to_dict(self._steam_dev)


