from django.shortcuts import render

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.models import ServiceOrder, Service


def modify_service(request):
    oders = ServiceOrder.objects.filter(is_active=True).order_by('-date_scheduled')
    page_obj = Pagination(request, oders)
    context = {
        "page_obj": page_obj,
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/modify_service.html", context=context)


def add_service(request):
    id = request.GET.get('id')
    if id:
        service = Service.objects.filter(id=id).first()
        context = {
            'service': service
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/service_management/add_service_basic.html", context=context)

    services = Service.objects.all()
    context = {
        'services': services
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/add_service.html", context=context)


def analyze_service(request):
    context = {

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/analyze_service.html", context=context)


def service_info(request):
    id = request.GET.get('id')
    serviceorder = ServiceOrder.objects.filter(id=id, is_active=True).first()
    context = {
        'item': serviceorder
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/service_management/service_info.html", context=context)
