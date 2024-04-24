# Generated by Django 4.2.10 on 2024-04-23 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0035_event_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="userip",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="登录时间"
            ),
        ),
        migrations.AlterField(
            model_name="userip",
            name="count",
            field=models.IntegerField(
                blank=True, default=0, null=True, verbose_name="访问次数"
            ),
        ),
        migrations.AlterField(
            model_name="userip",
            name="end_point",
            field=models.CharField(
                blank=True,
                default="/",
                max_length=30,
                null=True,
                verbose_name="访问端点",
            ),
        ),
        migrations.AlterField(
            model_name="userip",
            name="ip",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="IP 地址"
            ),
        ),
        migrations.AlterField(
            model_name="userip",
            name="ip_addr",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="IP 地理位置"
            ),
        ),
    ]
