from rest_framework import serializers, fields
from game_info.models import GameInfo
from steam_dev.models import SteamDevAPPS
from django.http import Http404


class GameInfoSerializer(serializers.ModelSerializer):

    #game = fields.SerializerMethodField('get_game')

    class Meta:
        model = GameInfo
        fields = ('game', 'name', 'chess', 'action', 'eaten',
                  'fromx', 'fromy', 'tox', 'toy')

