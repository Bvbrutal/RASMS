# Generated by Django 4.2.10 on 2024-04-23 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0037_userip_user_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="elder",
            name="bind_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="elder_data",
                to="app.user",
                verbose_name="绑定用户",
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="bind_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="staff_data",
                to="app.user",
                verbose_name="绑定用户",
            ),
        ),
        migrations.AlterField(
            model_name="volunteer",
            name="bind_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="volunteer_data",
                to="app.user",
                verbose_name="绑定用户",
            ),
        ),
    ]