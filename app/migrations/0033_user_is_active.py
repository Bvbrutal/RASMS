# Generated by Django 4.2.10 on 2024-04-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0032_remove_elder_avatar_photo_elder_elder_photo_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="是否有效"),
        ),
    ]
