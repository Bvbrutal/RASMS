# Generated by Django 4.2.10 on 2024-04-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0041_alter_user_grade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="grade",
            field=models.CharField(
                choices=[
                    ("0", "管理员"),
                    ("1", "工作人员"),
                    ("2", "老年用户"),
                    ("3", "义工用户"),
                    ("4", "其他"),
                ],
                default="3",
                max_length=1,
                verbose_name="类别",
            ),
        ),
    ]
