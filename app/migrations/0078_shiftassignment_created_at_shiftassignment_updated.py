# Generated by Django 4.2.10 on 2024-05-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0077_shiftassignment_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftassignment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='shiftassignment',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]