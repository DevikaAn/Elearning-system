# Generated by Django 4.2.3 on 2023-08-19 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0053_alter_content_chapter_text_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='Image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
