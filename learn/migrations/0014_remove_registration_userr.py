# Generated by Django 3.0.6 on 2020-12-13 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0013_registration_userr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='userr',
        ),
    ]