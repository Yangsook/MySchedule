# Generated by Django 4.2.9 on 2024-01-09 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_alter_event_memo_alter_person_history_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='eday',
            new_name='day',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eduration',
            new_name='duration',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='eprice',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='etime',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='etitle',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='sday',
            new_name='day',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='sduration',
            new_name='duration',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='sprice',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='stime',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='stitle',
            new_name='title',
        ),
    ]
