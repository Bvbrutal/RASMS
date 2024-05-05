# Generated by Django 4.2.10 on 2024-05-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_service_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='additional_costs',
            field=models.TextField(blank=True, null=True, verbose_name='附加费用'),
        ),
        migrations.AddField(
            model_name='service',
            name='customer_reviews',
            field=models.TextField(blank=True, null=True, verbose_name='客户评价'),
        ),
        migrations.AddField(
            model_name='service',
            name='qualifications',
            field=models.TextField(blank=True, null=True, verbose_name='服务人员资质'),
        ),
        migrations.AddField(
            model_name='service',
            name='service_area',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='服务区域'),
        ),
        migrations.AddField(
            model_name='service',
            name='service_hours',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='服务时间'),
        ),
        migrations.AddField(
            model_name='service',
            name='target_group',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='服务对象'),
        ),
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.CharField(blank=True, choices=[('daily_care', '日常护理'), ('medical_care', '医疗护理'), ('rehabilitation', '康复护理'), ('leisure', '休闲活动')], max_length=20, null=True, verbose_name='服务类型'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='服务描述'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='服务名称'),
        ),
    ]
