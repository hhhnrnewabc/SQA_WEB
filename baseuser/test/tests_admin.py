from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import (ModelAdmin, TabularInline,
     HORIZONTAL, VERTICAL)
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

        self.site = AdminSite()

    def test_default_fields(self):
        ma = BaseUserAdmin(BaseUser, self.site)
        # useradmin = admin.site._registry.get(BaseUser, None)

        self.assertEqual(list(ma.get_form(request).base_fields),
            ['email', 'password1', 'password2', 'is_active', 'is_staff',
             'groups', 'user_permissions'])

    def test_default_fieldsets(self):
        ma = BaseUserAdmin(BaseUser, self.site)
        self.assertEqual(ma.get_fieldsets(request),
            (
             (None,
              {'classes': ('wide',),
               'fields': ('email',
                          'password1',
                          'password2',
                          'is_active',
                          'is_staff',
                          'groups',
                          'user_permissions'
                          )
               }
              ),
            )
        )

    def test_get_fieldsets(self):

        class BandAdmin(ModelAdmin):
            def get_fieldsets(self, request, obj=None):
                return [(None,
                         {'classes': ('wide',),
                          'fields': ('email',
                                     'is_active',
                                     'is_staff',
                                     'groups',
                                     'user_permissions'
                                     )
                          }
                         )
                        ]

        ma = BandAdmin(BaseUser, self.site)
        form = ma.get_form(None)
        self.assertEqual(form._meta.fields,
            ['email', 'is_active', 'is_staff', 'groups', 'user_permissions'])

        # test inline from
        user = SteamUserInline(BaseUser, self.site)
        user_form = user.get_formset(request).form
        self.assertEqual(user_form._meta.fields, ['baseuser',
                                                  'first_name',
                                                  'last_name',
                                                  'nick_name',
                                                  'cell_phone',
                                                  'sex',
                                                  'photo',
                                                  'created',
                                                  'api_token',
                                                  'secret_token'])

        dev = SteamDeveloperInline(BaseUser, self.site)
        dev_form = dev.get_formset(request).form
        self.assertEqual(dev_form._meta.fields, ['baseuser',
                                                 'steam_user',
                                                 'first_name',
                                                 'last_name',
                                                 'address',
                                                 'work_phone',
                                                 'fax',
                                                 'company_name',
                                                 'api_token',
                                                 'secret_token',
                                                 'created'])


class BaseUserAdminFormTestCase(TestCase):
    def setUp(self):
        from django.utils.translation import activate
        activate('en-us')
        self.buser = BaseUser.objects.create(
            email="XX@yy.com",
            password="1234",
            is_active=True
        )

    def test_user_creation_form(self):
        # test email has already been registered
        form_data = {'password1': '1234',
                     'password2': '1234',
                     'email': "XX@yy.com",
                     'is_staff': False,
                     }
        form = UserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors,
            {'email': ['This email has already been registered.']})

        form_data = {'password1': '1234',
                     'password2': '4321',
                     'email': "YY@yy.com",
                     'is_staff': False,
                     }
        form = UserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {'password1': '1234',
                     'password2': '1234',
                     'email': "YY@yy.com",
                     'is_staff': False,
                     }
        form = UserCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        user = form.save()
        self.assertEqual(BaseUser.objects.get(email="YY@yy.com"), user)

    def test_user_change_form(self):
        form_data = {'email': 'YY@yy.com',
                     'password': "1234",
                     'is_active': False,
                     'is_staff': False,
                     'is_superuser': False,
                     }
        form = UserChangeForm(data=form_data)
        form.initial = form_data
        self.assertEqual(form.clean_password(), '1234')
