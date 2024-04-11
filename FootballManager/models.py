from django.db import models


class Footballer(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    name = models.CharField(max_length=100)
    surname = models.TextField(max_length=100)
    team_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Team(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    name = models.CharField(max_length=100)
    footballers_ids = models.ExpressionList(models.IntegerField())
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_lost = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    minute = models.IntegerField(blank=False, default=0)
    match_type = models.CharField(max_length=100)
    footballer_id = models.IntegerField(unique=True)
    match_id = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return f"{self.match_type} {self.minute}"


class Match(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    host_team_id = models.IntegerField(unique=True)
    guest_team_id = models.IntegerField(unique=True)
    host_goals = models.IntegerField(default=0)
    guest_goals = models.IntegerField(default=0)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return f"{self.host_goals} {self.guest_goals}"


class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('Footballer', on_delete=models.CASCADE)
    priority = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.name} - {self.status}"


class Statistic(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('Footballer', on_delete=models.CASCADE)
    season = models.CharField(max_length=20, null=True)
    matches_played = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} - {str(self.season)}"

