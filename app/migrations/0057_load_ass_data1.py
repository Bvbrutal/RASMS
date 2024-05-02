from django.db import migrations
from django.utils import timezone
from django.db import transaction

def add_assignment_data(apps, schema_editor):
    Staff = apps.get_model('app', 'Staff')
    Volunteer = apps.get_model('app', 'Volunteer')
    StaffAssignment = apps.get_model('app', 'StaffAssignment')
    VolunteerAssignment = apps.get_model('app', 'VolunteerAssignment')

    # 创建并保存样本员工
    staff_member1 = Staff.objects.filter(id=1).first()
    staff_member2 = Staff.objects.filter(id=2).first()

    # 创建并保存样本义工
    volunteer1 = Volunteer.objects.filter(id=1).first()
    volunteer2 = Volunteer.objects.filter(id=2).first()

    # 员工分配
    staff_assignment1 = StaffAssignment.objects.create(staff=staff_member1, assigned_area="North Wing", shift_start=timezone.now(), shift_end=timezone.now() + timezone.timedelta(hours=8))
    staff_assignment2 = StaffAssignment.objects.create(staff=staff_member2, assigned_area="South Wing", shift_start=timezone.now(), shift_end=timezone.now() + timezone.timedelta(hours=8))

    # 义工分配
    volunteer_assignment1 = VolunteerAssignment.objects.create(volunteer=volunteer1, assigned_area="East Wing", shift_start=timezone.now(), shift_end=timezone.now() + timezone.timedelta(hours=4))
    volunteer_assignment2 = VolunteerAssignment.objects.create(volunteer=volunteer2, assigned_area="West Wing", shift_start=timezone.now(), shift_end=timezone.now() + timezone.timedelta(hours=4))


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_load_ass_data'),
    ]

    operations = [
        migrations.RunPython(add_assignment_data),
    ]
