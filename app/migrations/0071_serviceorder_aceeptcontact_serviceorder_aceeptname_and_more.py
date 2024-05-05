# Generated by Django 4.2.10 on 2024-05-05 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0070_serviceorder_date_accepted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='aceeptContact',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='服务接受者联系方式'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='aceeptName',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='服务接受者'),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('pending', '待处理'), ('accepted', '已完成'), ('in_progress', '进行中'), ('completed', '已完成'), ('cancelled', '已取消')], default='pending', max_length=20, verbose_name='订单状态'),
        ),
    ]
