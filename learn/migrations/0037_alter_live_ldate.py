# Generated by Django 4.2.3 on 2023-07-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0036_remove_live_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='live',
            name='ldate',
            field=models.TimeField(null=True),
        ),
    ]