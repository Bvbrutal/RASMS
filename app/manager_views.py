from django.shortcuts import render

from app.models import Test, Elder
from app.user_views import GENDER_CHOICES, USER_TYPES


# pages
def index(request):
    return render(request, "manager/index_manager.html")


def profile(request):
    for key, value in request.session.items():
        print(f'{key}: {value}')
    mobile_phone = request.session["info"]["mobile_phone"]
    search_result = Test.objects.filter(mobile_phone=mobile_phone).first()
    user_id = search_result.user_id
    username = search_result.username
    phone = search_result.phone
    email = search_result.email
    bio = search_result.bio
    grade = USER_TYPES[str(search_result.grade)]
    gender = GENDER_CHOICES[search_result.gender]
    context = {
        'username': username,
        'user_id': user_id,
        'mobile_phone': mobile_phone,
        'bio': bio,
        'grade': grade,
        'phone': phone,
        'email': email,
        'gender': gender
    }
    return render(request, "manager/profile.html", context=context)


def select_event(request):
    return render(request, "manager/select_event.html")


# 老年人信息管理
def add_old(request):
    return render(request, "manager/elder_management/add_old.html")


def select_old(request):
    return render(request, "manager/elder_management/select_old.html")


def modify_old(request):
    return render(request, "manager/elder_management/modify_old.html")


def analyze_old(request):
    return render(request, "manager/elder_management/analyze_old.html")


def old_info(request):
    return render(request, "manager/elder_management/old_info.html")


def list_old(request):
    Elders=Elder.objects.all()
    print(Elders)
    context={
        "Elders":Elders,
    }
    return render(request, "manager/elder_management/list_old.html",context=context)


def modify_old_basic(request):
    return render(request, "manager/elder_management/modify_old_basic.html")


def modify_old_guardian(request):
    return render(request, "manager/elder_management/modify_old_guardian.html")


# 工作人员信息管理
def add_worker(request):
    return render(request, "manager/worker_management/add_worker.html")


def select_worker(request):
    return render(request, "manager/worker_management/select_worker.html")


def modify_worker(request):
    return render(request, "manager/worker_management/modify_worker.html")


def analyze_worker(request):
    return render(request, "manager/worker_management/analyze_worker.html")


def modify_worker_basic(request):
    return render(request, "manager/worker_management/modify_worker_basic.html")


def worker_info(request):
    return render(request, "manager/worker_management/worker_info.html")


# 义工信息管理
def add_volunteer(request):
    return render(request, "manager/volunteer_management/add_volunteer.html")


def select_volunteer(request):
    return render(request, "manager/volunteer_management/select_volunteer.html")


def modify_volunteer(request):
    return render(request, "manager/volunteer_management/modify_volunteer.html")


def analyze_volunteer(request):
    return render(request, "manager/volunteer_management/analyze_volunteer.html")


def volunteer_info(request):
    return render(request, "manager/volunteer_management/volunteer_info.html")


def modify_volunteer_basic(request):
    return render(request, "manager/volunteer_management/modify_volunteer_basic.html")


# 图表
def old_table(request):
    return render(request, "manager/data_manage/old_table.html")


def worker_table(request):
    return render(request, "manager/data_manage/worker_table.html")


def volunteer_table(request):
    return render(request, "manager/data_manage/volunteer_table.html")


def event_table(request):
    return render(request, "manager/data_manage/event_table.html")


def manager_table(request):
    return render(request, "manager/data_manage/manager_table.html")
