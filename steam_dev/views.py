from django.shortcuts import render
from steam_dev.form import CreateSteamDevForm
from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class UserDevView(FormView):
    template_name = 'steam_dev/user_profile.html'
    form_class = CreateSteamDevForm
    success_url = '/steam/user_profile/'
    _is_created = None
    _steam_user = None
    _steam_dev = None
    _user = None

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
                    messages.success(self.request, str(self._user.get_email) + ' Image Uploaded ')

                # new image is not allow to save
                # return old image
                # see form_class clean_photo setting
                else:
                    form.cleaned_data['photo'] = self._steam_user.photo
            except OSError:
                messages.error(self.request, str(self._user.get_email()) + ' Upload Failed ')

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