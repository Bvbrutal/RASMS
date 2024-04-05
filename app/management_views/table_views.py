# 图表
from django.shortcuts import render


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
