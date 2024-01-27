# Generated by Django 4.2.9 on 2024-01-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_schedule_created_schedule_modified_alter_event_etime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='modified',
        ),
        migrations.AlterField(
            model_name='event',
            name='ehours',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='etime',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='stime',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='volunteerhours',
            field=models.CharField(default='0', max_length=10),
        ),
    ]