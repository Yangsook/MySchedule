# Generated by Django 4.2.9 on 2024-01-09 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_alter_event_eduration_alter_schedule_sduration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
