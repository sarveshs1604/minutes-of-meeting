# Generated by Django 4.2.17 on 2024-12-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetingapp', '0003_event_duration_event_endtime_event_starttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]