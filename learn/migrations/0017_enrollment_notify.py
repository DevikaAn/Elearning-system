# Generated by Django 3.0.6 on 2020-12-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0016_registration_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='notify',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
