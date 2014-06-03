from steam_user.models import SteamUser
from django.forms import widgets
from rest_framework import serializers, fields


class SteamUserSerializer(serializers.ModelSerializer):
    photo = fields.SerializerMethodField('get_photo')

    class Meta:
        model = SteamUser
        fields = ('first_name', 'last_name', 'nick_name', 'id')
