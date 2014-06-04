from steam_user.models import SteamUser
from django.forms import widgets
from rest_framework import serializers, fields


class SteamUserSerializer(serializers.ModelSerializer):
    email = fields.SerializerMethodField('get_email')

    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'id', 'email')

    def get_email(self, obj):
        return '%s' % obj.baseuser.email
