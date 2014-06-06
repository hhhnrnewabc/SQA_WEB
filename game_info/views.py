from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from steam_dev.models import SteamDevAPPS
from game_info.models import GameInfo
from game_info.serializers import GameInfoSerializer
from django.http import Http404


class SteamDevAPPSGameInfo(APIView):

    def post(self, request, format=None):
        try:
            game = SteamDevAPPS.objects.get(api_token=request.DATA.get('api_token', None))
            data = request.DATA
            data.pop("api_token")
            data["game"] = game.id
        except SteamDevAPPS.DoesNotExist:
            raise Http404
        serializer = GameInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(selfr, request, format=None):
        app = GameInfo.objects.all()
        serializers = GameInfoSerializer(app, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

