# Generated by Django 4.2.9 on 2024-01-09 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0019_event_started'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='started',
            new_name='startdate',
        ),
    ]