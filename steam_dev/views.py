from django.shortcuts import render
from steam_dev.form import CreateSteamDevForm
from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict


class UserDevView(FormView):
    template_name = 'steam_dev/user_profile.html'
    form_class = CreateSteamDevForm
    success_url = '/steam/user_profile/'
    _is_created = None
    _steam_user = None
    _steam_dev = None
    _user = None

    def form_valid(self, form):

        return super(UserDevView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            self._user = user
            self._steam_user, is_created = SteamUser.objects.get_or_create(baseuser=self._user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))

        self._steam_dev, self._is_created = SteamDeveloper.objects.get_or_create(baseuser=self._user,
                                                                                 steam_user=self._steam_user)

        return super(UserDevView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # no image will return default image
        if self._is_created:
            self._steam_dev.update({'first_name': self._steam_user.first_name, 'last_name': self._steam_user.last_name})
            self._steam_dev.save()

        return model_to_dict(self._steam_dev)
