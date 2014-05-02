from django.contrib import admin
from steam_dev.models import (SteamDeveloper, SteamDevAPPS)


class SteamDevAPPSInline(admin.StackedInline):
    model = SteamDevAPPS
    readonly_fields = ('created', 'api_token', 'secret_token')


class SteamDeveloperAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['baseuser', 'steam_user']}),
    ]
    inlines = [SteamDevAPPSInline, ]
    list_display = ('baseuser', )
    list_filter = ['baseuser', ]
    search_fields = ['baseuser', 'steam_user']

admin.site.register(SteamDeveloper, SteamDeveloperAdmin)