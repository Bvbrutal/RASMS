# Generated by Django 4.2.10 on 2024-03-06 05:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_volunteer_staff_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='logging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('operation_content', models.TextField()),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.test')),
            ],
        ),
    ]
