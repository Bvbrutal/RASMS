from django.shortcuts import render

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.models import VolunteerAssignment, StaffAssignment


def regional_list(request):
    va=VolunteerAssignment.objects.filter(is_active=True)
    sa=StaffAssignment.objects.filter(is_active=True)
    context = {
        'va':va,
        'sa':sa

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/regional_list.html", context=context)


def modify_regional(request):
    context = {

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/modify_regional.html", context=context)




def add_regional(request):
    context = {

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/add_regional.html", context=context)



def analyze_regional(request):
    context = {

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/analyze_regional.html", context=context)


