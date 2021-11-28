# Generated by Django 3.2.7 on 2021-11-28 05:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0029_courses_discussion_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='date_time_of_last_edit',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(auto_now=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='message',
            name='date_time_of_last_edit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='replies',
            name='date_time_of_last_edit',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
