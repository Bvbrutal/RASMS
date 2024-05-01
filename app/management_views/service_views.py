from django.shortcuts import render

from app.components.Pagination import Pagination
from app.models import ServiceOrder


def modify_service(request):
    oders=ServiceOrder.objects.filter(is_active=True).order_by('-date_scheduled')
    page_obj = Pagination(request, oders)
    context = {
        "page_obj": page_obj,
    }
    context = {

    }
    return render(request, "manager/service_management/modify_service.html", context=context)


def add_service(request):
    context = {

    }
    return render(request, "manager/service_management/add_service.html", context=context)


def analyze_service(request):
    context = {

    }
    return render(request, "manager/service_management/analyze_service.html", context=context)


