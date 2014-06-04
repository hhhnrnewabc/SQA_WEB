from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.forms.models import model_to_dict
from steam_user.models import SteamUser
from steam_user.form import SteamUserForm
from django.views.generic.edit import FormView
from django.http import Http404
from django.contrib import messages
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SQA_Project.Digg_like_paginator import DiggPaginator
import datetime
import random

next_pudate_time = None
user_list = []


# user_list update, interval of at least 10 minutes
def get_user_list():
    global user_list, next_pudate_time
    now = datetime.datetime.now()
    if not next_pudate_time or now > next_pudate_time:
        next_pudate_time = now + datetime.timedelta(minutes=10)
        user_list = SteamUser.objects.filter(baseuser__is_superuser=False,
                                             baseuser__is_staff=False,
                                             baseuser__is_active=True)
    return user_list


def index(request):
    user_list_count = len(get_user_list())
    random4_user = []
    while len(random4_user) < 4:
        u = get_user_list()[random.randrange(0, user_list_count)]
        if u not in random4_user:
            random4_user.append(u)

    return render_to_response('steam_user/index.html',
                              {"random4_user": random4_user},
                              context_instance=RequestContext(request))


def list_all_user(request):
    paginator = DiggPaginator(get_user_list(), 10, body=2, margin=2, tail=2)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('steam_user/list_all_user.html',
                              {"contacts": contacts,
                               },
                              context_instance=RequestContext(request))


from steam_user.serializers import SteamUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie


class search(APIView):

    # @csrf_exempt
    def post(sself, request, format="json"):
        user_list = []
        data = request.DATA
        if data:
            search_name = data.get('search', '')
            user_list = list(SteamUser.objects.filter(baseuser__is_superuser=False,
                                                      baseuser__is_staff=False,
                                                      baseuser__is_active=True,
                                                      first_name__contains=search_name))
            user_list += list(SteamUser.objects.filter(baseuser__is_superuser=False,
                                                       baseuser__is_staff=False,
                                                       baseuser__is_active=True,
                                                       last_name__contains=search_name))
            user_list += list(SteamUser.objects.filter(baseuser__is_superuser=False,
                                                       baseuser__is_staff=False,
                                                       baseuser__is_active=True,
                                                       nick_name__contains=search_name))
            user_list += list(SteamUser.objects.filter(baseuser__is_superuser=False,
                                                       baseuser__is_staff=False,
                                                       baseuser__is_active=True,
                                                       baseuser__email__contains=search_name))
            user_set = set(user_list)
            if user_list:
                serializer = SteamUserSerializer(user_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("", status=status.HTTP_200_OK)


def user_profile(request, user_id):
    try:
        user_profile = SteamUser.objects.get(id=user_id)
    except SteamUser.DoesNotExist:
        raise Http404

    return render_to_response('steam_user/user_profile.html',
                              {"user_profile": user_profile},
                              context_instance=RequestContext(request))


# def steam_user_profile_new(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print('Raw Data: %s' % request.body)
#             print("POST Data: %s" % request.POST)
#             print(request.POST.dict())
#     print(request.POST)

#     return render_to_response('steam_user/user_profile_new.html',
#                               {},
#                               context_instance=RequestContext(request))


class SteamUserView(FormView):
    template_name = 'steam_user/self_profile.html'
    form_class = SteamUserForm
    success_url = '/steam/user_profile/'
    _user = None
    _is_created = None
    _steam_user = None

    def form_valid(self, form):
        if self._is_created:
            form.instance.baseuser = self._user
            form.save()
        else:
            try:
                old_photo_name = self._steam_user.photo.name
                new_photo_name = None
                new_photo = form.cleaned_data.get('photo', False)
                if new_photo:
                    new_photo_name = new_photo.name

                # if there upload new image, delete old image
                if new_photo_name != '' and old_photo_name != '' \
                        and new_photo_name != settings.USER_DEFAULT_AVATAR_POHTO and new_photo_name != old_photo_name:
                    import os
                    # delete the previous image but not default images
                    if old_photo_name and old_photo_name != settings.USER_DEFAULT_AVATAR_POHTO:
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(old_photo_name)))
                    self._steam_user.update(form.cleaned_data)
                    messages.success(self.request, _('Image Upload Success'))

                # new image is not allow to save
                # return old image and save other data
                # see form_class clean_photo setting
                else:
                    form.cleaned_data['photo'] = self._steam_user.photo
                    self._steam_user.update(form.cleaned_data)
            except OSError:
                messages.error(self.request, _('Image Upload Fail'))
        messages.success(self.request, _("Update Success"))
        return super(SteamUserView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            self._user = user
            self._steam_user, self._is_created = SteamUser.objects.get_or_create(baseuser=self._user)
        else:
            return HttpResponseRedirect(reverse('steam:user_signup'))

        return super(SteamUserView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        # no image will return default image
        if self._steam_user.photo.name == '':
            default_photo = ImageFieldFile(_('Image'), field=FileField(), name=settings.USER_DEFAULT_AVATAR_POHTO)
            self._steam_user.photo = default_photo
            # save image path to db
            self._steam_user.update({'photo': default_photo})
        # load data form models to form
        # use model_to_dict(model_object) will return dict_data
        # get_initial need return dict_type data to init the form
        return model_to_dict(self._steam_user)

    def get_form_kwargs(self):
        kwargs = super(SteamUserView, self).get_form_kwargs()
        return kwargs
