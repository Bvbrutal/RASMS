from django.http import JsonResponse
from django.shortcuts import render

from app.components.Dynamic_inheritance import Dynamic_inheritance
from app.components.Pagination import Pagination
from app.management_views.configuration import items_per_page
from app.models import ShiftAssignment, User


def regional_list(request):
    shifts = ShiftAssignment.objects.filter(is_active=True)
    weeks = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    shifts_by_weekday = {}
    week = 1
    for i in weeks:
        shifts_by_weekday[i] = shifts.filter(weekday=week).order_by('shift')
        week += 1

    context = {
        'shifts_by_weekday': shifts_by_weekday,
    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/regional_list.html", context=context)


def modify_regional(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        shifts = ShiftAssignment.objects.filter(is_active=True).order_by('weekday')

        page_obj = Pagination(request, shifts, 6)
        context = {
            "page_obj": page_obj,
            "key": key
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/regional_management/modify_regional.html", context=context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    id = request.POST.get("id")
    op = request.POST.get("op")
    SA = ShiftAssignment.objects.filter(id=id).first()
    if op == 'delete_service':
        SA.is_active = False
        SA.updated_by = updated_by
        SA.save()
        context = {
            'ret': 1,
            'msg': "删除成功"
        }

        return JsonResponse(context, safe=False)

    context = {
        'ret': 2,
        'msg': "删除失败"
    }
    return JsonResponse(context, safe=False)



def modify_shift(request):
    if request.method == "GET":
        id = request.GET.get('id', '')
        shift = ShiftAssignment.objects.filter(is_active=True,id=id).first()

        context = {
            "item": shift,
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/regional_management/modify_shift.html", context=context)

    updated_by_id = request.session["info"]["user_id"]
    updated_by = User.objects.filter(user_id=updated_by_id).first()
    shift_id = request.POST.get('id')
    staff_name = request.POST.get('staff_name')
    staff_phone = request.POST.get('staff_phone')
    volunteer_name = request.POST.get('volunteer_name', '')
    volunteer_phone = request.POST.get('volunteer_phone', '')
    area = request.POST.get('area', '')
    weekday = request.POST.get('weekday')
    shift = request.POST.get('shift')
    SA = ShiftAssignment.objects.filter(id=shift_id).first()
    print(shift_id,staff_name,staff_phone,volunteer_name,volunteer_phone,area,weekday)
    if SA:
        SA.staff_name = staff_name
        SA.staff_phone = staff_phone
        SA.volunteer_name = volunteer_name
        SA.volunteer_phone = volunteer_phone
        SA.area = area
        SA.weekday = weekday
        SA.shift = shift
        SA.updated_by = updated_by
        SA.save()
        # 返回成功信息
        context = {'ret': 1, 'msg': "修改成功"}
        return JsonResponse(context, safe=False)

        # 如果记录不存在，返回失败信息
    context = {'ret': 2, 'msg': "修改失败，记录不存在"}
    return JsonResponse(context, safe=False)






def add_regional(request):
    context = {

    }
    template_name = Dynamic_inheritance(request)
    context['template_name'] = template_name
    return render(request, "manager/regional_management/add_regional.html", context=context)



def shift_info(request):
    if request.method == "GET":
        id = request.GET.get('id', '')
        shift = ShiftAssignment.objects.filter(is_active=True, id=id).first()
        print(id,)

        context = {
            "item": shift,
        }
        template_name = Dynamic_inheritance(request)
        context['template_name'] = template_name
        return render(request, "manager/regional_management/shift_info.html", context=context)
