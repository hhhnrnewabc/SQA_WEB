from django.shortcuts import render
from steam_dev.form import SteamDevForm, SteamDevAPPForm, SteamDevApplyForm
from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, loader


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


class SteamDevProfileView(FormView):
    template_name = 'steam_dev/dev_profile.html'
    form_class = SteamDevForm
    success_url = 'dev_profile'
    _steam_dev = None
    _user = None

    def form_valid(self, form):
        # Exclude readonly_fields for ReadOnlyFieldsMixin
        if self.form_class.readonly_fields:
            for k in self.form_class.readonly_fields:
                form.cleaned_data.pop(k, None)
        # UPDATE DATA
        self._steam_dev.update(form.cleaned_data)
        return super(SteamDevProfileView, self).form_valid(form)

    @steam_dev_required
    def dispatch(self, request, *args, **kwargs):
        return super(SteamDevProfileView, self).dispatch(request, *args, **kwargs)

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from steam_dev.serializers import SteamUserSerializer, SteamDeveloperSerializer ,SteamDevAPPSSerializer


def steam_dev_api_check(function):
    # print(function.__name__)
    if function.__name__ == 'post':
        def post(self, request, format=None):
            if request.DATA:
                data = request.DATA
                api_token = data.get('api_token', '')
                secret_token = data.get('secret_token', '')
                try:
                    dev_user = SteamDeveloper.objects.get(api_token=api_token, secret_token=secret_token)
                except SteamDeveloper.DoesNotExist:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                return function(self, request, format=format)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return post


class SteamUserList(APIView):
    """
    List all steam user.

    POST your Dev Api Token and Secret Token :

        {
            "api_token" : "Your Api Token",
            "secret_token" : "Your Secret Token"
        }

    if is correct will return:

        [
            {
                "first_name": "",
                "last_name": "",
                "nick_name": "",
                "cell_phone": "",
                "sex": "",
                "photo": "noImageAvailable300.png",
                "api_token": "...",
                "secret_token": "..."
            }
        ]
    """
    @csrf_exempt
    @steam_dev_api_check
    def post(self, request, format=None):
        steam_users = SteamUser.objects.filter(baseuser__is_superuser=False, baseuser__is_staff=False)
        serializer = SteamUserSerializer(steam_users, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SteamDeveloperList(APIView):
    """
    List all steam developer.

    POST your Dev Api Token and Secret Token :

        {
            "api_token" : "Your Api Token",
            "secret_token" : "Your Secret Token"
        }

    if is correct will return:

        [
            {
                "first_name": "",
                "last_name": "",
                "address": "",
                "work_phone": "",
                "fax": "",
                "company_name": "",
                "created": "2014-05-12T03:58:55Z"
            }
        ]
    """
    @csrf_exempt
    @steam_dev_api_check
    def post(self, request, format=None):
        steam_dev = SteamDeveloper.objects.filter(baseuser__is_superuser=False, baseuser__is_staff=False)
        serializer = SteamDeveloperSerializer(steam_dev, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def api_root(request, format=None):
    """
    API Root Page

    """
    # Assuming we have views named 'steam_user_list'
    # in our project's URLconf namespace 'steam_dev'.
    return Response({
        'Steam User List': reverse('steam_dev:steam_user_list', request=request, format=format),
        'Steam Developer List': reverse('steam_dev:steam_dev_list', request=request, format=format),
    })
