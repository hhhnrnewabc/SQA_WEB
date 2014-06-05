from django.test import TestCase
from steam_dev.models import SteamDeveloper, SteamDevAPPS, get_upload_file_name
from baseuser.models import BaseUser
from steam_user.models import SteamUser


class SteamDeveloperTestCase(TestCase):
    def setUp(self):
        # set defalut lang to English
        from django.utils.translation import activate
        activate('en-us')

        buser = BaseUser.objects.create_user(email="XX@yy.com", password="1234")
        buser.is_active = True
        buser.save()
        user = SteamUser.objects.create(
            baseuser=buser, first_name='F', last_name='L',
            nick_name='N', cell_phone='1234567890', sex="F"
            )
        self.dev = SteamDeveloper.objects.create(
            baseuser=buser, steam_user=user,
            first_name=user.first_name,
            last_name=user.last_name
            )

    def test_name(self):
        name = self.dev.get_full_name()
        name_str = str(self.dev)
        self.assertEqual(name, name_str)
        self.assertEqual(name, 'FL')

        update_dict = {'first_name': "FF", 'last_name': "LL"}
        self.dev.update(**update_dict)
        name = self.dev.get_full_name()
        self.assertEqual(name, 'FFLL')

        update_dict = {'first_name': "", 'last_name': ""}
        self.dev.update(**update_dict)
        name = self.dev.get_full_name()
        self.assertEqual(name, "<No Full Name>" + self.dev.baseuser.email)

    def test_key(self):
        key = self.dev.generate_key()
        self.assertEqual(len(key), 100)

        old_key = self.dev.secret_token
        self.dev.create_new_secret_token()
        new_ket = self.dev.secret_token

        self.assertNotEqual(old_key, new_ket)
        self.assertEqual(len(new_ket), 100)


class SteamDevAPPSTestCase(TestCase):
    def setUp(self):
        from django.utils.translation import activate
        activate('en-us')

        buser = BaseUser.objects.create_user(email="XX@yy.com", password="1234")
        buser.is_active = True
        buser.save()
        user = SteamUser.objects.create(
            baseuser=buser, first_name='F', last_name='L',
            nick_name='N', cell_phone='1234567890', sex="F"
            )
        dev = SteamDeveloper.objects.create(
            baseuser=buser, steam_user=user,
            first_name=user.first_name,
            last_name=user.last_name
            )
        self.app = SteamDevAPPS.objects.create(
            steam_dev=dev, web_url="123.com",
            app_name="app", app_introduction="is a app",
            )

    def test_name(self):
        name = str(self.app.steam_dev) + '-' + self.app.get_app_name()
        name_str = str(self.app)
        self.assertEqual(name, name_str)
        self.assertEqual(name, 'FL-app')

        update_dict = {'app_name': "new app"}
        self.app.update(**update_dict)
        name = self.app.get_app_name()
        self.assertEqual(name, 'new app')

    def test_key(self):
        key = self.app.generate_key()
        self.assertEqual(len(key), 100)

        old_key = self.app.secret_token
        self.app.create_new_secret_token()
        new_ket = self.app.secret_token

        self.assertNotEqual(old_key, new_ket)
        self.assertEqual(len(new_ket), 100)

    def test_upload_name(self):
        filename = 'p.jpeg'
        upload_file_name = get_upload_file_name(self.app, filename)
        upload_dir, user_dir, user_hash_dir, filename = upload_file_name.split('/')
        self.assertEqual(upload_dir, "uploaded_files")
        self.assertEqual(user_dir, "dev")
        self.assertEqual(len(user_hash_dir), 64)

        year, m, d = filename.split('_')[:3]
        from time import gmtime, strftime
        now_time = strftime("%Y_%m_%d", gmtime())
        Nyear, Nm, Nd = now_time.split('_')[:3]

        self.assertEqual(Nyear, year)
        self.assertEqual(Nm, m)
        self.assertEqual(Nd, d)
