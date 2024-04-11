# Generated by Django 5.0.4 on 2024-04-11 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FootballManager", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Teams",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("wins", models.IntegerField(default=0)),
                ("draws", models.IntegerField(default=0)),
                ("losses", models.IntegerField(default=0)),
                ("goals_scored", models.IntegerField(default=0)),
                ("goals_lost", models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name="footballers",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
