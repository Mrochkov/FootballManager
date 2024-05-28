# Generated by Django 5.0.3 on 2024-05-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FootballManager', '0021_remove_queue_matches_match_queue_alter_queue_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('GOAL', 'Gol'), ('ASSIST', 'Asysta'), ('YELLOW CARD', 'Żółta kartka'), ('RED CARD', 'Czerwona kartka'), ('OWN GOAL', 'Gol samobójczy')], default='GOAL', max_length=20),
        ),
    ]
