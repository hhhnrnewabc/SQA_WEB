from steam_user.models import SteamUser


# check the steam user name if not will show message
class CheckUserNameMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                steam_user = SteamUser.objects.get(baseuser=request.user)
                if not steam_user.first_name and not steam_user.last_name:
                    request.check_name = False
                else:
                    request.check_name = True
            except SteamUser.DoesNotExist:
                request.check_name = True
        # witout not login user
        else:
            request.check_name = True
