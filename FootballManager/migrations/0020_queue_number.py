# Generated by Django 5.0.3 on 2024-05-27 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FootballManager', '0019_team_description_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]