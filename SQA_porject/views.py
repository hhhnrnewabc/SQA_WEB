from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse


def steam_404_view(request):
    return render(request, 'polls/404.html',)