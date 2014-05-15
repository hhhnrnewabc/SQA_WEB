import pytz
from django.utils import timezone


# set Time Zone default is Asia/Taipei
class TimezoneMiddleware(object):
    def process_request(self, request):
        request.common_timezones = pytz.common_timezones
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
            # timezone.activate(pytz.timezone('Asia/Taipei'))


