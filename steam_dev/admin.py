from django.contrib import admin
from steam_dev.models import (SteamDeveloper, SteamDevAPPS)


class SteamDevAPPSInline(admin.StackedInline):
    model = SteamDevAPPS
    readonly_fields = ('created', 'api_token', 'secret_token')


class SteamDeveloperAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['baseuser', 'steam_user', 'first_name', 'last_name', 'address', 'work_phone', 'fax',
                           'company_name', 'created', ]}),
    ]
    inlines = [SteamDevAPPSInline, ]
    readonly_fields = ('created',)
    list_display = ('baseuser', )
    list_filter = ['baseuser', ]
    search_fields = ['baseuser', 'steam_user']


class SteamDevAPPSAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['steam_dev', 'web_url', 'created', ]}),
        ("APP", {'fields': ['app_name', 'app_introduction', ]}),
        ("Photo", {'fields': ['photo_big', 'photo_small', ]}),
        ("Api Token", {'fields': ['api_token', 'secret_token', ]}),
    ]
    readonly_fields = ('created',)
    list_display = ('steam_dev', )
    list_filter = ['steam_dev', ]
    search_fields = ['steam_dev', 'api_token']

admin.site.register(SteamDeveloper, SteamDeveloperAdmin)
admin.site.register(SteamDevAPPS, SteamDevAPPSAdmin)