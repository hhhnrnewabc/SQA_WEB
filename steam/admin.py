from django.contrib import admin
from steam.models import (Game, GameLanguages, GameVersions, GameUpdatedDate, GameReviews, GameSystemRequirements)


class GameLanguagesInline(admin.TabularInline):
    model = GameLanguages


class GameVersionsInline(admin.TabularInline):
    model = GameVersions


class GameUpdatedDateInline(admin.TabularInline):
    model = GameUpdatedDate


class GameReviewsInline(admin.TabularInline):
    model = GameReviews


class GameSystemRequirementsInline(admin.TabularInline):
    model = GameSystemRequirements


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'game_type', 'release_date', 'web_url', 'developer', 'publisher']})
    ]
    inlines = [GameLanguagesInline, GameVersionsInline, GameUpdatedDateInline, GameReviewsInline,
               GameSystemRequirementsInline]
    list_display = ('name', 'game_type', 'release_date', 'web_url', 'developer', 'publisher')
    list_filter = ('game_type', 'developer', 'publisher')
    search_fields = ('name', 'release_date', 'web_url', 'developer', 'publisher')


admin.site.register(Game, GameAdmin)

admin.site.register(GameLanguages)
admin.site.register(GameVersions)
admin.site.register(GameUpdatedDate)
admin.site.register(GameReviews)
admin.site.register(GameSystemRequirements)
