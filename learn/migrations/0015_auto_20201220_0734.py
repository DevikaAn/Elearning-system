# Generated by Django 3.0.6 on 2020-12-20 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0014_remove_registration_userr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='enrol_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='Exam_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='exam_results',
            name='Exam_res_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='Feed_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='learning_progress',
            name='Learn_p_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='requests',
            name='Req_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='Sub_reg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Registration'),
        ),
    ]
