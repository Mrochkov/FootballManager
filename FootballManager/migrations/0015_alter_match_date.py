# Generated by Django 5.0.3 on 2024-05-08 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FootballManager', '0014_alter_event_event_type_alter_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
