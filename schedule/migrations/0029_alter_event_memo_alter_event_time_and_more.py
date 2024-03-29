# Generated by Django 4.2.9 on 2024-01-14 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0028_schedule_dateday_schedule_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='memo',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='history',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='memo',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='memo',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
