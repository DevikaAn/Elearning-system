# Generated by Django 4.1.6 on 2023-02-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0020_alter_blogs_id_alter_enrollment_id_alter_exam_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]