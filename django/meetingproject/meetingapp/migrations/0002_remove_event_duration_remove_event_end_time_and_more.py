# Generated by Django 4.2.17 on 2024-12-06 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
    ]
