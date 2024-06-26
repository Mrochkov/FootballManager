# Generated by Django 5.0.4 on 2024-04-11 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FootballManager", "0002_teams_alter_footballers_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("surname", models.TextField(max_length=100)),
                ("team_id", models.IntegerField(unique=True)),
            ],
        ),
    ]
