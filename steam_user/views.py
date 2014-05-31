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


def index(request):
    return render(request, 'steam_user/index.html')


def list_all_user(request):
    user_list = SteamUser.objects.filter(baseuser__is_superuser=False,
                                         baseuser__is_staff=False,
                                         baseuser__is_active=True)
    paginator = DiggPaginator(user_list, 5, body=2, margin=2, tail=2)

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
                              {"contacts": contacts},
                              context_instance=RequestContext(request))


def user_profile(request, user_id):
    try:
        user_profile = SteamUser.objects.ger(id=user_id)
    except SteamUser.DoesNotExist:
        raise Http404

    return render_to_response('steam_user/user_profile.html',
                              {"user_profile": user_profile},
                              context_instance=RequestContext(request))


class SteamUserView(FormView):
    template_name = 'steam_user/user_profile.html'
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
                        and new_photo_name != settings.NO_IMAGE_AVAILABLE_PHOTO and new_photo_name != old_photo_name:
                    import os
                    # delete the previous image but not default images
                    if old_photo_name and old_photo_name != settings.NO_IMAGE_AVAILABLE_PHOTO:
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(old_photo_name)))
                    self._steam_user.update(form.cleaned_data)
                    messages.success(self.request, _(' Image Upload Success'))

                # new image is not allow to save
                # return old image and save other data
                # see form_class clean_photo setting
                else:
                    form.cleaned_data['photo'] = self._steam_user.photo
                    self._steam_user.update(form.cleaned_data)
            except OSError:
                messages.error(self.request, _('Image Upload Failed '))
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
            default_photo = ImageFieldFile(_('Image'), field=FileField(), name=settings.NO_IMAGE_AVAILABLE_PHOTO)
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
