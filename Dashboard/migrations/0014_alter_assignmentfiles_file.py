# Generated by Django 3.2.7 on 2021-10-18 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0013_auto_20211015_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentfiles',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
