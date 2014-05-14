from steam_user.models import SteamUser
from steam_dev.models import SteamDeveloper, SteamDevAPPS
from django.forms import widgets
from rest_framework import serializers, fields


class SteamUserSerializer(serializers.ModelSerializer):
    photo = fields.SerializerMethodField('get_photo')

    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'cell_phone', 'sex', 'photo', 'api_token', 'secret_token',
                  'created')

    def get_photo(self, obj):
        return '%s' % obj.photo.url


class SteamDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamDeveloper
        fields = ('first_name', 'last_name', 'address', 'work_phone', 'fax', 'company_name', 'created', )


class SteamDevAPPSSerializer(serializers.ModelSerializer):
    photo_big = fields.SerializerMethodField('get_photo_big')
    photo_small = fields.SerializerMethodField('get_photo_small')

    class Meta:
        model = SteamDevAPPS
        fields = ('web_url', 'created', 'app_name', 'app_introduction',
                  'photo_big', 'photo_small', 'api_token', 'secret_token', )

    def get_photo_big(self, obj):
        return '%s' % obj.photo_big.url

    def get_photo_small(self, obj):
        return '%s' % obj.photo_small.url