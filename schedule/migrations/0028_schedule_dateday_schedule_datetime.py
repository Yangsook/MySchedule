# Generated by Django 4.2.9 on 2024-01-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0027_remove_schedule_dateday_remove_schedule_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='dateday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='datetime',
            field=models.TimeField(null=True),
        ),
    ]
