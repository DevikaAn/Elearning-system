# Generated by Django 4.2.3 on 2023-08-03 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0052_alter_assignment_assign_course_alter_chapter_cha_cou_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='Chapter_text_content',
            field=models.TextField(max_length=900, null=True),
        ),
    ]