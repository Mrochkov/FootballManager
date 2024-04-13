# Generated by Django 5.0.4 on 2024-04-13 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("FootballManager", "0010_team_footballers_alter_event_event_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="events",
        ),
        migrations.RemoveField(
            model_name="statistic",
            name="minutes_played",
        ),
        migrations.RemoveField(
            model_name="statistic",
            name="season",
        ),
        migrations.RemoveField(
            model_name="team",
            name="footballers",
        ),
    ]
