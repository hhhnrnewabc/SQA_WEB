from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
import pytz


def steam_404_view(request):
    return render(request, 'steam/404.html',)


def set_timezone(request):

    if request.method == 'POST':
        next = request.POST['next']
        request.session['django_timezone'] = request.POST['timezone']
        if next == "":
            # return HttpResponseRedirect(reverse('steam:index'))
            return redirect('/')
        else:
            return HttpResponseRedirect(next)
    else:
        raise Http404

