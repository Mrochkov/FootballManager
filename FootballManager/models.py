from datetime import datetime, timezone

from django.db import models


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_lost = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Footballer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team', null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    minute = models.IntegerField(blank=False, default=0)
    footballer = models.ForeignKey('Footballer', on_delete=models.CASCADE, null=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True)

    class EventType(models.TextChoices):
        GOAL = 'GOAL', 'Goal'
        YELLOW_CARD = 'YELLOW CARD', 'Yellow card'
        RED_CARD = 'RED CARD', 'Red card'

    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.GOAL)

    def __str__(self):
        return f"{self.event_type} {self.minute}"


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    host_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='host_team', null=True)
    guest_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='guest_team', null=True)
    date = models.DateTimeField(null=True)
    host_goals = models.IntegerField(default=0)
    guest_goals = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.host_goals} {self.guest_goals}"


class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    matches = models.ManyToManyField('Match')

    def __str__(self):
        return f"{self.matches}"


class Statistic(models.Model):
    id = models.AutoField(primary_key=True)
    footballer = models.ForeignKey('Footballer', on_delete=models.CASCADE)
    matches_played = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.footballer.name}"

