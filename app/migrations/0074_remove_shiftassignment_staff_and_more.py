# Generated by Django 4.2.10 on 2024-05-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0073_alter_shiftassignment_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiftassignment',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='shiftassignment',
            name='volunteer',
        ),
        migrations.AddField(
            model_name='shiftassignment',
            name='staff_name',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='工作人员'),
        ),
        migrations.AddField(
            model_name='shiftassignment',
            name='staff_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='工作人员联系方式'),
        ),
        migrations.AddField(
            model_name='shiftassignment',
            name='volunteer_name',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='义工'),
        ),
        migrations.AddField(
            model_name='shiftassignment',
            name='volunteer_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='义工联系方式'),
        ),
    ]