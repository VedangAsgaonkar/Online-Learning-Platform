# Generated by Django 3.2.7 on 2021-11-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0024_message_replies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
