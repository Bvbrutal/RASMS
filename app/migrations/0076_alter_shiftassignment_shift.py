# Generated by Django 4.2.10 on 2024-05-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0075_remove_volunteerassignment_volunteer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftassignment',
            name='shift',
            field=models.IntegerField(blank=True, choices=[(1, '时间段 1: 08:00-10:20'), (2, '时间段 2: 10:20-12:40'), (3, '时间段 3: 12:40-15:00'), (4, '时间段 4: 15:00-17:20'), (5, '时间段 5: 17:20-19:40'), (6, '时间段 6: 19:40-22:00')], null=True, verbose_name='班次'),
        ),
    ]