from django.db import models, transaction


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    trainer = models.CharField(max_length=60)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_lost = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    description = models.TextField(blank=True)

    def matches_played(self):
        return Match.objects.filter(models.Q(host_team=self) | models.Q(guest_team=self)).count()

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
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True, related_name='events')

    def update_statistics(self):
        if self.event_type == self.EventType.GOAL:
            Statistic.objects.filter(footballer=self.footballer).update(goals_scored=models.F('goals_scored') + 1)
        elif self.event_type == self.EventType.ASSIST:
            Statistic.objects.filter(footballer=self.footballer).update(assists=models.F('assists') + 1)
        elif self.event_type == self.EventType.YELLOW_CARD:
            Statistic.objects.filter(footballer=self.footballer).update(yellow_cards=models.F('yellow_cards') + 1)
        elif self.event_type == self.EventType.RED_CARD:
            Statistic.objects.filter(footballer=self.footballer).update(red_cards=models.F('red_cards') + 1)
        elif self.event_type == self.EventType.OWN_GOAL:
            Statistic.objects.filter(footballer=self.footballer).update(own_goals=models.F('own_goals') + 1)

    def update_match_score(self):
        if self.event_type == self.EventType.GOAL:
            if self.match.host_team == self.footballer.team:
                self.match.host_goals += 1
            elif self.match.guest_team == self.footballer.team:
                self.match.guest_goals += 1
        elif self.event_type == self.EventType.OWN_GOAL:
            if self.match.host_team == self.footballer.team:
                self.match.guest_goals += 1
            elif self.match.guest_team == self.footballer.team:
                self.match.host_goals += 1
        self.match.save()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.update_statistics()
            self.update_match_score()

    class EventType(models.TextChoices):
        GOAL = 'GOAL', 'Gol'
        ASSIST = 'ASSIST', 'Asysta'
        YELLOW_CARD = 'YELLOW CARD', 'Żółta kartka'
        RED_CARD = 'RED CARD', 'Czerwona kartka'
        OWN_GOAL = 'OWN GOAL', 'Gol samobójczy'

    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.GOAL)

    def __str__(self):
        return f"{self.event_type} {self.minute}"


class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return f"Kolejka {self.number}"

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    host_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='host_team', null=True)
    guest_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='guest_team', null=True)
    date = models.DateTimeField(null=True)
    host_goals = models.IntegerField(null=True)
    guest_goals = models.IntegerField(null=True)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='matches', null=True)

    def __str__(self):
        return f"{self.host_team} {self.host_goals} - {self.guest_goals} {self.guest_team}"


class Statistic(models.Model):
    id = models.AutoField(primary_key=True)
    footballer = models.ForeignKey('Footballer', on_delete=models.CASCADE)
    matches_played = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    own_goals = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.footballer.name}"

