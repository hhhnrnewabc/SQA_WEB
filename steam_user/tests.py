from django.test import TestCase
from steam_user.models import SteamUser, StreamFriends, get_upload_file_name
from baseuser.models import BaseUser


class SteamUserTestCase(TestCase):

    def setUp(self):
        # set defalut lang to English
        from django.utils.translation import activate
        activate('en-us')

        xx = BaseUser.objects.create_superuser(email="XX@yy.com", password="1234")
        self.sx = SteamUser.objects.create(baseuser=xx, first_name='F', last_name='L',
            nick_name='N', cell_phone='1234567890', sex="F")

    def test_key(self):
        key = self.sx.generate_key()
        self.assertEqual(len(key), 100)

        old_key = self.sx.secret_token
        self.sx.create_new_secret_token()
        new_ket = self.sx.secret_token

        self.assertNotEqual(old_key, new_ket)
        self.assertEqual(len(new_ket), 100)

    def test_name(self):
        name = self.sx.get_full_name()
        name_str = self.sx.__str__()
        self.assertEqual(name, 'FL')
        self.assertEqual(name, name_str)

        update_dict = {'first_name': "FF", 'last_name': "LL"}
        self.sx.update(update_dict)
        new_name = self.sx.get_full_name()
        self.assertEqual(new_name, "FFLL")

        update_dict = {'first_name': "", 'last_name': ""}
        self.sx.update(update_dict)
        new_name = self.sx.get_full_name()
        self.assertEqual(new_name, "<No Full Name>XX@yy.com")

    def test_upload_name(self):
        filename = 'p.jpeg'
        upload_file_name = get_upload_file_name(self.sx, filename)
        upload_dir, user_dir, user_hash_dir, filename = upload_file_name.split('/')
        self.assertEqual(upload_dir, "uploaded_files")
        self.assertEqual(user_dir, "user")
        self.assertEqual(len(user_hash_dir), 64)

        year, m, d = filename.split('_')[:3]
        from time import gmtime, strftime
        now_time = strftime("%Y_%m_%d", gmtime())
        Nyear, Nm, Nd = now_time.split('_')[:3]
        self.assertEqual(Nyear, year)
        self.assertEqual(Nm, m)
        self.assertEqual(Nd, d)
