# Generated by Django 4.2.10 on 2024-05-13 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0078_shiftassignment_created_at_shiftassignment_updated"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Registration",
        ),
    ]