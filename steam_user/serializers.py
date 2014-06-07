from steam_user.models import SteamUser
from steam_user.models import SteamUserOnlineToken
from django.forms import widgets
from rest_framework import serializers, fields


class SteamUserSerializer(serializers.ModelSerializer):
    email = fields.SerializerMethodField('get_email')

    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'id', 'email')

    def get_email(self, obj):
        return '%s' % obj.baseuser.email


class SteamUserOnlineCheckSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField('get_user_name')

    class Meta:
        model = SteamUserOnlineToken
        fields = ('user',)

    def get_user_name(self, obj):
        return '%s' % obj.user.get_full_name()

