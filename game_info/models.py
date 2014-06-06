from django.db import models
from steam_dev.models import SteamDevAPPS


class GameRelation(models.Model):

    game = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            app = SteamDevAPPS.objects.get(id=self.game)
            self.name = str(app.steam_dev) + app.app_name
            return super(GameRelation, self).save(*args, **kwargs)
        except SteamDevAPPS.DoesNotExist:
            pass

    # def update_game(self, game, commit=True, *args, **kwargs):
    #     try:
    #         m = GameRelation.objects.get(game=game.id)
    #         m.game = game.id
    #         m.name = game.app_name
    #         m.save()
    #     except GameRelation.DoesNotExist:
    #         pass

    # def update_games(self, games, commit=True, *args, **kwargs):
    #     for g in games:
    #         try:
    #             m = GameRelation.objects.get(game=g.id)
    #             if m.name != g.name:
    #                 m.name = g.name
    #                 m.save()
    #         except GameRelation.DoesNotExist:
    #             m = GameRelation.objects.create(name=g.app_name, game=g.id)
    #             m.save()


class GameInfo(models.Model):
    game = models.ForeignKey(GameRelation, null=True)

    name = models.CharField(max_length=20)
    chess = models.CharField(max_length=20)

    action = models.CharField(max_length=20)
    eaten = models.CharField(max_length=20)

    fromx = models.CharField(max_length=5)
    fromy = models.CharField(max_length=5)
    tox = models.CharField(max_length=5)
    toy = models.CharField(max_length=5)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

