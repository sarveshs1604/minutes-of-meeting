# Generated by Django 4.2.17 on 2024-12-11 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetingapp', '0008_alter_event_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='agenda',
            field=models.JSONField(default=list),
        ),
    ]
