from django.contrib import admin
from .models import *


class FootballerInline(admin.TabularInline):
    model = Footballer
    extra = 1


class QueueInline(admin.TabularInline):
    model = Queue
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'wins', 'draws', 'losses', 'goals_scored', 'goals_lost', 'trainer', 'matches_played')
    search_fields = ('name', 'trainer')
    list_filter = ('trainer', 'wins', 'name')
    fields = ('name', 'trainer', 'wins', 'draws', 'losses', 'goals_scored', 'goals_lost', 'logo', 'description')
    inlines = [FootballerInline]


@admin.register(Footballer)
class FootballerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'team')
    search_fields = ('name', 'surname', 'team__name')
    list_filter = ('team',)


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('host_team', 'guest_team', 'date', 'host_goals', 'guest_goals')
    search_fields = ('host_team__name', 'guest_team__name')
    list_filter = ('host_team', 'guest_team', 'date')
    inlines = [EventInline]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('minute', 'footballer', 'match', 'event_type')
    search_fields = ('footballer__name', 'footballer__surname')
    list_filter = ('event_type',)


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount_of_matches')
    search_fields = ('matches__id',)

    def amount_of_matches(self, obj):
        return obj.matches.count()


@admin.register(Statistic)
class Statistic(admin.ModelAdmin):
    list_display = ('footballer', 'matches_played', 'goals_scored', 'assists', 'yellow_cards', 'red_cards')
    search_fields = ('footballer__name', 'footballer__surname')
