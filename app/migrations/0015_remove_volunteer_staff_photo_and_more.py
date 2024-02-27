# Generated by Django 4.2.10 on 2024-03-02 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_name_volunteer_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='staff_photo',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='volunteer_photo',
            field=models.ImageField(blank=True, null=True, upload_to='volunteer_photo/'),
        ),
    ]