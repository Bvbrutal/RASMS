# Generated by Django 4.2.10 on 2024-05-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0064_service_count_alter_service_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitnumber',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='计数类型'),
        ),
    ]
