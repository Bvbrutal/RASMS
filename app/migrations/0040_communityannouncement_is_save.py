# Generated by Django 4.2.10 on 2024-04-25 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0039_logging_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityannouncement",
            name="is_save",
            field=models.BooleanField(default=True, verbose_name="是否保存为草稿"),
        ),
    ]