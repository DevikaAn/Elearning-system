# Generated by Django 4.2 on 2023-07-17 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0026_registration_registration_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_tim', models.DateTimeField(auto_now_add=True, null=True)),
                ('Attendance_done_location', models.CharField(max_length=200, null=True)),
                ('atten_stud', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.registration')),
            ],
        ),
    ]
