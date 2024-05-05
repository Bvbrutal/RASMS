# Generated by Django 4.2.10 on 2024-05-03 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_service_created_at_alter_service_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_Service_created', to='app.user', verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='service',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='service',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_Service_updated', to='app.user', verbose_name='更新人'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_ServiceOrder_created', to='app.user', verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_ServiceOrder_updated', to='app.user', verbose_name='更新人'),
        ),
        migrations.AlterField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
    ]