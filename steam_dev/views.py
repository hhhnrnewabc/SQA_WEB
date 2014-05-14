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
                    return Response({"detail": "FORBIDDEN"}, status=status.HTTP_400_BAD_REQUEST)
                return function(self, request, format=format)
            return Response({"detail": "NO POST DATA"}, status=status.HTTP_400_BAD_REQUEST)
        return post


class SteamUserList(APIView):
    """
    List all steam user.

    ----------------------------------------------------------------------------------------------------------------

    POST your dev `api_token` and `secret_token` :

        {
            "api_token" : "Your_Api_Token",
            "secret_token" : "Your_Secret_Token"
        }

    If is correct will return:

        [
            {
                "first_name": "",
                "last_name": "",
                "nick_name": "",
                "cell_phone": "",
                "sex": "",
                "photo": "/media/noImageAvailable300.png",
                "api_token": "...",
                "secret_token": "...",
                "created": "2014-05-12T03:58:55Z"
            }
        ]

    ----------------------------------------------------------------------------------------------------------------

    ##Data Type:
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value Type</th>
          <th>Max length</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td> first_name    </td>
          <td>       string  </td>
          <td> 30           </td>
        </tr>
        <tr>
          <td> last_name     </td>
          <td>       string  </td>
          <td> 30           </td>
        </tr>
        <tr>
          <td> nick_name     </td>
          <td>       string  </td>
          <td> 30           </td>
        </tr>
        <tr>
          <td> cell_phone    </td>
          <td>       string  </td>
          <td> 20           </td>
        </tr>
        <tr>
          <td> sex           </td>
          <td>       string  </td>
          <td> 1            </td>
        </tr>
        <tr>
          <td> photo         </td>
          <td>          url  </td>
          <td> 200          </td>
        </tr>
        <tr>
          <td> api_token     </td>
          <td>       string  </td>
          <td> 100          </td>
        </tr>
        <tr>
          <td> secret_token  </td>
          <td>       string  </td>
          <td> 100          </td>
        </tr>
        <tr>
          <td> created       </td>
          <td>       string  </td>
          <td> 20*           </td>
        </tr>
      </tbody>
    </table>

    ----------------------------------------------------------------------------------------------------------------

    ###sex:
    <table class="table table-striped">
      <thead>
        <tr>
          <th>     code </th>
          <th> representation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>        F </td>
          <td>        Female </td>
        </tr>
        <tr>
          <td>        M </td>
          <td>          Male </td>
        </tr>
        <tr>
          <td>        O </td>
          <td>         Other </td>
        </tr>
      </tbody>
    </table>

    ----------------------------------------------------------------------------------------------------------------

    ###photo:
    example photo_path: `/media/noImageAvailable300.png`

    domain url: `https://sqa.swim-fish.info` + photo_path

    Location is: `https://sqa.swim-fish.info/media/noImageAvailable300.png`

    ----------------------------------------------------------------------------------------------------------------

    ###token:
    length 100

    composition: `a`to`z` or `0`to`9`

    ----------------------------------------------------------------------------------------------------------------

    ###created:
    example: `2014-05-13T15:44:05Z`

    **year**`-`**month**`-`**day**`T`**hour**`:`**minute**`:`**second**`Z`


    <table class="table table-striped">
      <thead>
        <tr>
          <th> time unit </th>
          <th>    number length </th>
          <th> example </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>      year </td>
          <td>                4  </td>
          <td>    2014 </td>
        </tr>
        <tr>
          <td>     month </td>
          <td>                2  </td>
          <td>      05 </td>
        </tr>
        <tr>
          <td>       day </td>
          <td>                2  </td>
          <td>      13 </td>
        </tr>
        <tr>
          <td>      hour </td>
          <td> 2 (24-hour clock) </td>
          <td>      15 </td>
        </tr>
        <tr>
          <td>    minute </td>
          <td>                2  </td>
          <td>      44 </td>
        </tr>
        <tr>
          <td>    second </td>
          <td>                2  </td>
          <td>      05 </td>
        </tr>
      </tbody>
    </table>

    """
    @csrf_exempt
    @steam_dev_api_check
    def post(self, request, format=None):
        steam_users = SteamUser.objects.filter(baseuser__is_superuser=False, baseuser__is_staff=False)
        serializer = SteamUserSerializer(steam_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SteamDeveloperList(APIView):
    """
    List all steam developer.
    -----------------------

    POST your dev `api_token` and `secret_token` :

        {
            "api_token" : "Your_Api_Token",
            "secret_token" : "Your_Secret_Token"
        }

    If is correct will return:

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

    ----------------------------------------------------------------------------------------------------------------

    ##Data Type:
    <table class="table table-striped">
      <thead>
        <tr>
          <th> Key           </th>
          <th> Value Type    </th>
          <th> Max length   </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td> first_name    </td>
          <td>       string  </td>
          <td> 30           </td>
        </tr>
        <tr>
          <td> last_name     </td>
          <td>       string  </td>
          <td> 30           </td>
        </tr>
        <tr>
          <td> address       </td>
          <td>       string  </td>
          <td> 200          </td>
        </tr>
        <tr>
          <td> work_phone    </td>
          <td>       string  </td>
          <td> 20           </td>
        </tr>
        <tr>
          <td> fax           </td>
          <td>       string  </td>
          <td> 20           </td>
        </tr>
        <tr>
          <td> company_name  </td>
          <td>       string  </td>
          <td> 50           </td>
        </tr>
        <tr>
          <td> created       </td>
          <td>         time  </td>
          <td> 20*           </td>
        </tr>
      </tbody>
    </table>

    ----------------------------------------------------------------------------------------------------------------


    ###created:
    example: `2014-05-13T15:44:05Z`

    **year**`-`**month**`-`**day**`T`**hour**`:`**minute**`:`**second**`Z`


    <table class="table table-striped">
      <thead>
        <tr>
          <th> time unit </th>
          <th>    number length  </th>
          <th> example </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>      year </td>
          <td> 4                 </td>
          <td>    2014 </td>
        </tr>
        <tr>
          <td>     month </td>
          <td> 2                 </td>
          <td>      05 </td>
        </tr>
        <tr>
          <td>       day </td>
          <td> 2                 </td>
          <td>      13 </td>
        </tr>
        <tr>
          <td>      hour </td>
          <td> 2 (24-hour clock) </td>
          <td>      15 </td>
        </tr>
        <tr>
          <td>    minute </td>
          <td> 2                 </td>
          <td>      44 </td>
        </tr>
        <tr>
          <td>    second </td>
          <td> 2                 </td>
          <td>      05 </td>
        </tr>
      </tbody>
    </table>

    """
    @csrf_exempt
    @steam_dev_api_check
    def post(self, request, format=None):
        steam_dev = SteamDeveloper.objects.filter(baseuser__is_superuser=False, baseuser__is_staff=False)
        serializer = SteamDeveloperSerializer(steam_dev, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
def api_root(request, format=None):
    """
    ##IF you want to use this API, You have to sign up a dev account.

    ##Get your `api_token` and `secret_token`

    ##Detailed usage instructions, please refer to the following link.

    ----------------------------------------------------------------------------------------------------------------

    POST use curl :

        curl -k https://sqa.swim-fish.info/steam/dev/api/steam_user_list
             -H "Content-Type: application/json"
             -d '{
                    "api_token":"Your_Api_Token",
                    "secret_token":"Your_Secret_Token"
                 }'

    `-k` for https \n
    `-H` Http Head \n
    `-d` POST DATA \n

    ----------------------------------------------------------------------------------------------------------------

    ###ERROR CODE:
    <table class="table table-striped">
      <tr>
        <th>POST Type</th>
        <th>ERROR CODE</th>
        <th>Representation</th>
      </tr>
      <tr>
        <td rowspan="3">application/json</td>
        <td>"detail": "JSON parse error - Expecting value:..."</td>
        <td>JSON format is wrong</td>
      </tr>
      <tr>
        <td>"detail": "FORBIDDEN"</td>
        <td><code>api_token</code> or <code>secret_token</code> not correct</td>
      </tr>
      <tr>
        <td>"detail": "Method 'GET' not allowed."</td>
        <td>GET not allowed</td>
      </tr>
      <tr>
        <td>application/x-www-form-urlencoded</td>
        <td>"detail": "NO POST DATA"</td>
        <td>POST Data is empty</td>
      </tr>
      <tr>
        <td>multipart/form-data</td>
        <td>"detail": "Multipart form parse error - Invalid Content-Type: application/x-www-form-urlencoded"</td>
        <td>Multipart form format is wrong</td>
      </tr>
    </table>

    """
    # Assuming we have views named 'steam_user_list'
    # in our project's URLconf namespace 'steam_dev'.
    return Response({
        'Steam User List': reverse('steam_dev:steam_user_list', request=request, format=format),
        'Steam Developer List': reverse('steam_dev:steam_dev_list', request=request, format=format),
    })
