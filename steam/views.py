from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from steam.models import Game


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

    # if username == "" or password == "":
    #     return HttpResponseRedirect( reverse('polls:index' ) )

    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            if next == "":
                return HttpResponseRedirect( reverse('steam:index' ) )
            else:
                return HttpResponseRedirect(next)
            # return render_to_response('polls/index.html', { 'login_success':"Login Success", },
            #     context_instance=RequestContext(request, default_context ) )

        else:
            # Return a 'disabled account' error message
            return render_to_response('steam/login.html', {'login_faill': "disabled account", },
                context_instance=RequestContext(request))

    else:
        # Return an 'invalid login' error message.
        return render_to_response('steam/login.html',
                                  {'login_faill': "invalid login", }, context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return render_to_response('steam/index.html', {'logout_success': "Logout Success", },
                              context_instance=RequestContext(request, ))

