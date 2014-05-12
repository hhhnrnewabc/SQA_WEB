from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper, SteamDevAPPS
from django.forms import widgets
from rest_framework import serializers


class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'cell_phone', 'sex', 'photo', 'api_token', 'secret_token', )


class SteamDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamDeveloper
        fields = ('first_name', 'last_name', 'address', 'work_phone', 'fax', 'company_name', 'created', )


class SteamDevAPPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamDevAPPS
        fields = ('web_url', 'created', 'app_name', 'app_introduction',
                  'photo_big', 'photo_small', 'api_token', 'secret_token', )