# Generated by Django 3.2.7 on 2021-10-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_alter_assignments_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='access_code',
            field=models.CharField(default='12345678', max_length=32),
        ),
        migrations.AddField(
            model_name='courses',
            name='course_info',
            field=models.CharField(default='Course Info', max_length=1000),
        ),
        migrations.AddField(
            model_name='courses',
            name='master_code',
            field=models.CharField(default='12345678', max_length=32),
        ),
    ]
