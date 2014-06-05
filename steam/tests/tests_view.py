from django.test import TestCase
from steam_user.models import SteamUser, StreamFriends, get_upload_file_name
from baseuser.models import BaseUser
from django.test.client import Client
from django.utils import translation
from django.utils import timezone


class SteamUserViewTestCase(TestCase):

    def setUp(self):
        # set defalut lang to English
        from django.utils.translation import activate
        activate('en-us')

        xx = BaseUser.objects.create_user(email="XX@yy.com", password="1234")
        xx.is_active = True
        xx.save()
        self.sx = SteamUser.objects.create(baseuser=xx, first_name='F', last_name='L',
            nick_name='N', cell_phone='1234567890', sex="F")

    def test_login_logout(self):
        c = Client()
        response = c.post('/steam/login/', {'Email': 'XX@yy.com', 'UserPassword': '1234'})
        response.status_code
        self.assertEqual(response.status_code, 200)

        response = c.post('/steam/userLogout/')
        self.assertEqual(response.status_code, 302)

    def test_change_lang(self):
        c = Client()
        self.assertEqual(translation.get_language(), 'en-us')
        response = c.post('/i18n/setlang/', {'language': 'zh-tw'})
        response.status_code
        self.assertEqual(response.status_code, 302)
        self.assertEqual(translation.get_language(), 'zh-tw')

    def test_change_time_zone(self):
        c = Client()
        self.assertEqual(timezone.get_current_timezone_name(), 'UTC')
        response = c.post('/time_zone/', {'timezone': 'Asia/Taipei', 'next': ''})
        response.status_code
        c.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(timezone.get_current_timezone_name(), 'Asia/Taipei')
