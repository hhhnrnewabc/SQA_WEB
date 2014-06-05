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
        response = c.get('/')
        response = c.get('/steam/login/')
        self.assertEqual(response.status_code, 200)

        response = c.post('/steam/userLogin/', {'Email': 'XX@yy.com', 'UserPassword': '1234'})
        self.assertEqual(response.status_code, 302)

        response = c.get('/steam/userLogin/')
        self.assertEqual(response.status_code, 302)

        c.logout()

        response = c.post('/steam/userLogin/?next=/steam', {'Email': 'XX@yy.com', 'UserPassword': '1234'})
        self.assertEqual(response.status_code, 302)

        c.logout()

        response = c.post('/steam/userLogin/', {'Email': 'XX@yy.com', 'UserPassword': '4321'})
        response = c.get('/')

        is_login = c.login(email='XX@yy.com', password='1234')
        self.assertEqual(is_login, True)
        response = c.get('/steam/user_profile/')
        self.assertEqual(response.status_code, 200)

        response = c.get('/steam/userLogout/')
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

    def test_game_index(self):
        c = Client()
        response = c.get('/steam/game/')
        self.assertEqual(response.status_code, 200)
