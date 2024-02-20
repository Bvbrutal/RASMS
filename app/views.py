from django.shortcuts import render


# 注册登录
def login(request):
    return render(request, "account/login.html")


def register(request):
    return render(request, "account/register.html")


# pages
def index(request):
    return render(request, "page/index.html")


def profile(request):
    return render(request, "account/profile.html")


def select_event(request):
    return render(request, "account/select_event.html")


# 老年人信息管理
def add_old(request):
    return render(request, "elder_management/add_old.html")


def select_old(request):
    return render(request, "elder_management/select_old.html")


def modify_old(request):
    return render(request, "elder_management/modify_old.html")


def analyze_old(request):
    return render(request, "elder_management/analyze_old.html")


# 工作人员信息管理
def add_worker(request):
    return render(request, "worker_management/add_worker.html")


def select_worker(request):
    return render(request, "worker_management/select_worker.html")


def modify_worker(request):
    return render(request, "worker_management/modify_worker.html")


def analyze_worker(request):
    return render(request, "worker_management/analyze_worker.html")


# 义工信息管理
def add_volunteer(request):
    return render(request, "volunteer_management/add_volunteer.html")


def select_volunteer(request):
    return render(request, "volunteer_management/select_volunteer.html")


def modify_volunteer(request):
    return render(request, "volunteer_management/modify_volunteer.html")


def analyze_volunteer(request):
    return render(request, "volunteer_management/analyze_volunteer.html")


def volunteer_info(request):
    return render(request, "page/volunteer_info.html")


def old_table(request):
    return render(request, "data_manage/old_table.html")


def worker_table(request):
    return render(request, "data_manage/worker_table.html")


def volunteer_table(request):
    return render(request, "data_manage/volunteer_table.html")


def event_table(request):
    return render(request, "data_manage/event_table.html")


def manager_table(request):
    return render(request, "data_manage/manager_table.html")