# Generated by Django 4.2.3 on 2023-07-20 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0032_live'),
    ]

    operations = [
        migrations.RenameField(
            model_name='live',
            old_name='Date',
            new_name='lDate',
        ),
        migrations.AddField(
            model_name='live',
            name='link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
