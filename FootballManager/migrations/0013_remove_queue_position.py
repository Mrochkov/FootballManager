# Generated by Django 5.0.4 on 2024-04-24 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "FootballManager",
            "0012_rename_status_queue_position_remove_queue_created_at_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="queue",
            name="position",
        ),
    ]
