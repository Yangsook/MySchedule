# Generated by Django 4.2.9 on 2024-01-09 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0020_rename_started_event_startdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='enddate',
            field=models.DateField(null=True),
        ),
    ]
