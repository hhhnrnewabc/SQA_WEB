from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import (ModelAdmin, TabularInline,
     HORIZONTAL, VERTICAL)
from steam_dev.admin import (SteamDeveloperAdmin, SteamDevAPPSAdmin,
    SteamDevAPPSInline)
from steam_dev.models import SteamDeveloper, SteamDevAPPS


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True


class MockSuperDev(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class SteamDeveloperAdminTestCase(TestCase):
    def setUp(self):
        from django.utils.translation import activate
        activate('en-us')
        self.site = AdminSite()

    def test_default_fields(self):
        ma = SteamDeveloperAdmin(SteamDeveloper, self.site)

        self.assertEqual(list(ma.get_form(request).base_fields),
            ['baseuser',
             'steam_user',
             'first_name',
             'last_name',
             'address',
             'work_phone',
             'fax',
             'company_name'])

    def test_default_fieldsets(self):
        ma = SteamDeveloperAdmin(SteamDeveloper, self.site)
        self.assertEqual(ma.get_fieldsets(request),
            [(None, {'fields': ['baseuser', 'steam_user',
                                'first_name', 'last_name',
                                'address', 'work_phone',
                                'fax', 'company_name',
                                'created'
                                ]
                     }
              )]
        )

    def test_get_fieldsets(self):

        class BandAdmin(ModelAdmin):
            def get_fieldsets(self, request, obj=None):
                return [(None, {'fields': ['baseuser', 'steam_user',
                                           'first_name', 'last_name',
                                           'address', 'work_phone',
                                           'fax', 'company_name',
                                           ]
                                }
                         )]
        ma = BandAdmin(SteamDeveloper, self.site)
        form = ma.get_form(None)
        self.assertEqual(form._meta.fields,
            ['baseuser', 'steam_user', 'first_name', 'last_name', 'address',
             'work_phone', 'fax', 'company_name'])

        # inline
        dev = SteamDevAPPSInline(SteamDeveloper, self.site)
        dev_form = dev.get_formset(request).form
        self.assertEqual(dev_form._meta.fields,
            ['steam_dev', 'web_url',
             'app_name', 'app_introduction',
             'photo_big', 'photo_small',
             'created',
             'api_token', 'secret_token']
            )


class SteamDevAPPSAdminTestCase(TestCase):
    def setUp(self):
        from django.utils.translation import activate
        activate('en-us')
        self.site = AdminSite()

    def test_default_fields(self):
        ma = SteamDevAPPSAdmin(SteamDevAPPS, self.site)

        self.assertEqual(list(ma.get_form(request).base_fields),
            ['steam_dev',
             'web_url',
             'app_name',
             'app_introduction',
             'photo_big',
             'photo_small',
             'api_token',
             'secret_token'])

    def test_default_fieldsets(self):
        ma = SteamDevAPPSAdmin(SteamDevAPPS, self.site)
        self.assertEqual(ma.get_fieldsets(request),
            [(None, {'fields': ['steam_dev', 'web_url', 'created', ]}),
             ("APP", {'fields': ['app_name', 'app_introduction', ]}),
             ("Photo", {'fields': ['photo_big', 'photo_small', ]}),
             ("Api Token", {'fields': ['api_token', 'secret_token', ]}),
             ]
        )

    def test_get_fieldsets(self):

        class BandAdmin(ModelAdmin):
            def get_fieldsets(self, request, obj=None):
                return [(None, {'fields': ['steam_dev',
                                           'app_name', 'app_introduction',
                                           'photo_big', 'photo_small',
                                           ]
                                }
                         )]
        ma = BandAdmin(SteamDevAPPS, self.site)
        form = ma.get_form(None)
        self.assertEqual(form._meta.fields,
            ['steam_dev', 'app_name', 'app_introduction',
             'photo_big', 'photo_small'])
