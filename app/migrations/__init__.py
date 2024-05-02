# Generated by Django 3.2 on 2023-10-04

from django.db import migrations

def add_schedule_data(apps, schema_editor):
    Staff = apps.get_model('your_app_name', 'Staff')
    Volunteer = apps.get_model('your_app_name', 'Volunteer')

    # 添加工作人员排班数据
    staff_data = [
        {'username': 'Alice', 'assigned_area': '北区', 'shift_start': '09:00', 'shift_end': '17:00'},
        {'username': 'Bob', 'assigned_area': '南区', 'shift_start': '10:00', 'shift_end': '18:00'}
    ]

    for staff in staff_data:
        Staff.objects.create(**staff)

    # 添加义工排班数据
    volunteer_data = [
        {'username': 'Charlie', 'assigned_area': '东区', 'shift_start': '08:00', 'shift_end': '12:00'},
        {'username': 'Diana', 'assigned_area': '西区', 'shift_start': '13:00', 'shift_end': '17:00'}
    ]

    for volunteer in volunteer_data:
        Volunteer.objects.create(**volunteer)

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', 'previous_migration_file'),
    ]

    operations = [
        migrations.RunPython(add_schedule_data),
    ]
