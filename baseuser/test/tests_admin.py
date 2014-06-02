from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from django.contrib.admin.sites import AdminSite
from baseuser.admin import (BaseUserAdmin, UserChangeForm,
     UserCreationForm, SteamDeveloperInline, SteamUserInline)
from baseuser.models import BaseUser
from django.core import mail


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class BaseUserAdminTestCase(TestCase):
    def setUp(self):
        from django.utils.translation import activate
        activate('en-us')
        self.buser = BaseUser.objects.create(
            email="XX@yy.com",
            password="1234",
            is_active=True
        )
        self.site = AdminSite()

    def test_default_fields(self):
        ma = BaseUserAdmin(BaseUser, self.site)

        self.assertEqual(list(ma.get_form(request).base_fields),
            ['email', 'password1', 'password2', 'is_active', 'is_staff',
             'groups', 'user_permissions'])
